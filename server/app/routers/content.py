from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..activity import record_activity
from ..content import CARDS, PROBLEMS, PROBLEMS_BY_ID, TOPICS, TOPICS_BY_ID
from ..content.patterns import PATTERNS, TECHNIQUES
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


@router.get("/search")
def search(q: str = "", limit: int = 5):
    term = q.strip().lower()
    if len(term) < 2:
        return {"topics": [], "problems": [], "flashcards": []}

    def matches(*fields):
        return any(term in field.lower() for field in fields)

    return {
        "topics": [
            {"id": t["id"], "title": t["title"]}
            for t in TOPICS if matches(t["title"], t["summary"])
        ][:limit],
        "problems": [
            {"id": p["id"], "title": p["title"]}
            for p in PROBLEMS if matches(p["title"])
        ][:limit],
        "flashcards": [
            {"id": c["id"], "title": c["front"], "topic": c["topic"]}
            for c in CARDS if matches(c["front"], c["back"])
        ][:limit],
    }


@router.get("/daily")
def daily_problem():
    # The same problem for everyone on a given UTC day.
    problem = PROBLEMS[date.today().toordinal() % len(PROBLEMS)]
    return {"problem": problem_summary(problem)}


@router.get("/patterns")
def patterns():
    return {
        "techniques": TECHNIQUES,
        "questions": [
            {"question": question, "answer": answer, "why": why}
            for question, answer, why in PATTERNS
        ],
    }


@router.get("/cheatsheet")
def cheatsheet():
    return {
        "topics": [
            {"id": topic["id"], "title": topic["title"], "complexity": topic["complexity"]}
            for topic in TOPICS
        ]
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
        record_activity(db, user.id)
        db.commit()

    return {"score": score, "total": len(quiz), "results": results}
