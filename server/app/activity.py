from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import ActivityDay, now


def record_activity(db: Session, user_id: int) -> None:
    """Mark today (UTC) as a study day. The caller commits."""
    today = now().date()
    if db.get(ActivityDay, (user_id, today)) is None:
        db.add(ActivityDay(user_id=user_id, day=today))


def streaks(days: list[date], today: date) -> dict:
    active = set(days)
    longest = run = 0
    previous = None
    for day in sorted(active):
        run = run + 1 if previous and day - previous == timedelta(days=1) else 1
        longest = max(longest, run)
        previous = day

    # A streak survives until the end of the next day, so yesterday still counts.
    cursor = today if today in active else today - timedelta(days=1)
    current = 0
    while cursor in active:
        current += 1
        cursor -= timedelta(days=1)
    return {"current": current, "longest": longest, "activeToday": today in active}


def user_streaks(db: Session, user_id: int) -> dict:
    days = db.scalars(select(ActivityDay.day).where(ActivityDay.user_id == user_id)).all()
    return streaks(list(days), now().date())
