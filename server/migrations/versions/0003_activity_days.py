"""Study days, for streaks.

Revision ID: 0003
Revises: 0002
Create Date: 2026-10-30
"""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "activity_days",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("day", sa.Date, primary_key=True),
    )


def downgrade():
    op.drop_table("activity_days")
