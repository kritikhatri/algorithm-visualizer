"""Flashcard spaced-review progress.

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-28
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "flashcard_progress",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("card_id", sa.String(80), primary_key=True),
        sa.Column("box", sa.Integer, nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table("flashcard_progress")
