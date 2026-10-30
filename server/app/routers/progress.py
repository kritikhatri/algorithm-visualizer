from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..activity import record_activity, user_streaks
from ..content import PROBLEMS_BY_ID, TOPICS_BY_ID
from ..db import get_db
from ..models import ProblemProgress, QuizAttempt, TopicProgress, User, now
from ..security import current_user

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/progress")
def get_progress(user: User = Depends(current_user), db: Session = Depends(get_db)):
    topics = db.scalars(select(TopicProgress).where(TopicProgress.user_id == user.id)).all()
    problems = db.scalars(select(ProblemProgress).where(ProblemProgress.user_id == user.id)).all()
    best_scores = db.execute(
        select(QuizAttempt.topic_id, func.max(QuizAttempt.score), func.max(QuizAttempt.total))
        .where(QuizAttempt.user_id == user.id)
        .group_by(QuizAttempt.topic_id)
    ).all()
    recent_quizzes = db.scalars(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(5)
    ).all()

    return {
        "streak": user_streaks(db, user.id),
        "completedTopics": [row.topic_id for row in topics],
        "solvedProblems": [row.problem_id for row in problems if row.solved_at],
        "attemptedProblems": [row.problem_id for row in problems if not row.solved_at],
        "quizBest": {topic_id: {"score": score, "total": total}
                     for topic_id, score, total in best_scores},
        "recentQuizzes": [
            {"topic": row.topic_id, "score": row.score, "total": row.total,
             "createdAt": row.created_at.isoformat()}
            for row in recent_quizzes
        ],
        "recentlySolved": [
            {"problem": row.problem_id, "solvedAt": row.solved_at.isoformat()}
            for row in sorted(
                (row for row in problems if row.solved_at),
                key=lambda row: row.solved_at,
                reverse=True,
            )[:5]
        ],
    }


@router.put("/progress/topics/{topic_id}", status_code=204)
def complete_topic(topic_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if topic_id not in TOPICS_BY_ID:
        raise HTTPException(404, "Topic not found.")
    if db.get(TopicProgress, (user.id, topic_id)) is None:
        db.add(TopicProgress(user_id=user.id, topic_id=topic_id))
        record_activity(db, user.id)
        db.commit()
    return Response(status_code=204)


@router.delete("/progress/topics/{topic_id}", status_code=204)
def uncomplete_topic(topic_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)):
    row = db.get(TopicProgress, (user.id, topic_id))
    if row is not None:
        db.delete(row)
        db.commit()
    return Response(status_code=204)


class Attempt(BaseModel):
    code: str = Field(max_length=20_000)
    passed: bool


def find_problem(problem_id: str) -> None:
    if problem_id not in PROBLEMS_BY_ID:
        raise HTTPException(404, "Problem not found.")


@router.get("/problems/{problem_id}/progress")
def get_problem_progress(
    problem_id: str, user: User = Depends(current_user), db: Session = Depends(get_db)
):
    find_problem(problem_id)
    row = db.get(ProblemProgress, (user.id, problem_id))
    if row is None:
        return {"code": None, "solved": False, "attempts": 0}
    return {"code": row.code, "solved": row.solved_at is not None, "attempts": row.attempts}


@router.put("/problems/{problem_id}/progress")
def save_attempt(
    problem_id: str,
    body: Attempt,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    find_problem(problem_id)
    row = db.get(ProblemProgress, (user.id, problem_id))
    if row is None:
        row = ProblemProgress(user_id=user.id, problem_id=problem_id, attempts=0)
        db.add(row)

    row.code = body.code
    row.attempts += 1
    record_activity(db, user.id)
    if body.passed and row.solved_at is None:
        row.solved_at = now()
    db.commit()
    return {"solved": row.solved_at is not None, "attempts": row.attempts}
