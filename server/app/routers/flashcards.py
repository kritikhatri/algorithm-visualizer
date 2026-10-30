from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..content import CARDS, CARDS_BY_ID, TOPICS_BY_ID
from ..db import get_db
from ..models import FlashcardProgress, User, now
from ..security import current_user

router = APIRouter(prefix="/api", tags=["flashcards"])

# Leitner system: a correct answer moves a card up a box, a miss sends it back to box 1.
# Higher boxes are reviewed less often.
MAX_BOX = 4
INTERVAL_DAYS = {1: 1, 2: 3, 3: 7, 4: 14}
NEW_CARDS_PER_SESSION = 10


def cards_for(topic: str | None) -> list[dict]:
    if topic and topic not in TOPICS_BY_ID:
        raise HTTPException(404, "Topic not found.")
    return [card for card in CARDS if topic in (None, card["topic"])]


def as_utc(moment):
    # SQLite returns naive datetimes in tests; Postgres returns aware ones.
    return moment if moment.tzinfo else moment.replace(tzinfo=now().tzinfo)


@router.get("/flashcards")
def list_flashcards(topic: str | None = None):
    return {"cards": cards_for(topic)}


@router.get("/review")
def review_queue(
    topic: str | None = None,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    cards = cards_for(topic)
    rows = {
        row.card_id: row
        for row in db.scalars(select(FlashcardProgress).where(FlashcardProgress.user_id == user.id))
    }
    current = now()

    due = sorted(
        (
            {**card, "box": rows[card["id"]].box}
            for card in cards
            if card["id"] in rows and as_utc(rows[card["id"]].due_at) <= current
        ),
        key=lambda card: card["box"],
    )
    new = [{**card, "box": 0} for card in cards if card["id"] not in rows]

    seen = [rows[card["id"]] for card in cards if card["id"] in rows]
    return {
        "due": due,
        "new": new[:NEW_CARDS_PER_SESSION],
        "stats": {
            "total": len(cards),
            "seen": len(seen),
            "due": len(due),
            "mastered": sum(row.box == MAX_BOX for row in seen),
            "boxes": [sum(row.box == box for row in seen) for box in range(1, MAX_BOX + 1)],
        },
    }


class Answer(BaseModel):
    correct: bool


@router.post("/review/{card_id}")
def answer_card(
    card_id: str,
    body: Answer,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
):
    if card_id not in CARDS_BY_ID:
        raise HTTPException(404, "Card not found.")

    row = db.get(FlashcardProgress, (user.id, card_id))
    if row is None:
        row = FlashcardProgress(user_id=user.id, card_id=card_id, box=0)
        db.add(row)

    row.box = min(row.box + 1, MAX_BOX) if body.correct else 1
    row.reviewed_at = now()
    row.due_at = row.reviewed_at + timedelta(days=INTERVAL_DAYS[row.box])
    db.commit()
    return {"box": row.box, "dueAt": row.due_at.isoformat()}
