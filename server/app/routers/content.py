from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..content import PROBLEMS, PROBLEMS_BY_ID, TOPICS, TOPICS_BY_ID
from ..db import get_db
from ..models import QuizAttempt, User
from ..security import optional_user

router = APIRouter(prefix="/api", tags=["content"])

PROBLEM_SUMMARY_FIELDS = ("id", "title", "topic", "difficulty")


def problem_summary(problem: dict) -> dict:
    return {field: problem[field] for field in PROBLEM_SUMMARY_FIELDS}


def find_topic(topic_id: str) -> dict:
    topic = TOPICS_BY_ID.get(topic_id)
    if topic is None:
        raise HTTPException(404, "Topic not found.")
    return topic


@router.get("/topics")
def list_topics():
    return {
        "topics": [
            {
                "id": topic["id"],
                "title": topic["title"],
                "category": topic["category"],
                "summary": topic["summary"],
                "problemCount": len(topic["problems"]),
                "quizCount": len(topic["quiz"]),
            }
            for topic in TOPICS
        ]
    }


@router.get("/topics/{topic_id}")
def get_topic(topic_id: str):
    topic = find_topic(topic_id)
    return {
        "topic": {
            **{key: topic[key] for key in ("id", "title", "category", "summary", "visualizer",
                                           "lesson", "complexity", "snippets")},
            "problems": [problem_summary(problem) for problem in topic["problems"]],
        }
    }


@router.get("/problems")
def list_problems():
    return {"problems": [problem_summary(problem) for problem in PROBLEMS]}


@router.get("/problems/{problem_id}")
def get_problem(problem_id: str):
    problem = PROBLEMS_BY_ID.get(problem_id)
    if problem is None:
        raise HTTPException(404, "Problem not found.")
    return {"problem": problem}


@router.get("/topics/{topic_id}/quiz")
def get_quiz(topic_id: str):
    topic = find_topic(topic_id)
    return {
        "questions": [
            {"question": item["question"], "options": item["options"]}
            for item in topic["quiz"]
        ]
    }


class QuizSubmission(BaseModel):
    answers: list[int | None]


@router.post("/topics/{topic_id}/quiz")
def submit_quiz(
    topic_id: str,
    body: QuizSubmission,
    user: User | None = Depends(optional_user),
    db: Session = Depends(get_db),
):
    quiz = find_topic(topic_id)["quiz"]
    if len(body.answers) != len(quiz):
        raise HTTPException(400, f"Expected {len(quiz)} answers.")

    results = [
        {
            "correct": answer == item["answer"],
            "answer": item["answer"],
            "explanation": item["explanation"],
        }
        for answer, item in zip(body.answers, quiz)
    ]
    score = sum(result["correct"] for result in results)

    if user is not None:
        db.add(QuizAttempt(user_id=user.id, topic_id=topic_id, score=score, total=len(quiz)))
        db.commit()

    return {"score": score, "total": len(quiz), "results": results}
