"""Study platform tables; move accounts over from the old Prisma schema.

Revision ID: 0001
Revises:
Create Date: 2026-10-24
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("username", sa.String(20), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "topic_progress",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("topic_id", sa.String(50), primary_key=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "problem_progress",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("problem_id", sa.String(80), primary_key=True),
        sa.Column("code", sa.Text, nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False),
        sa.Column("solved_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "quiz_attempts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"),
                  nullable=False, index=True),
        sa.Column("topic_id", sa.String(50), nullable=False),
        sa.Column("score", sa.Integer, nullable=False),
        sa.Column("total", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    # Carry accounts over from the previous Node/Prisma backend, if it ran here.
    tables = sa.inspect(op.get_bind()).get_table_names()
    if "User" in tables:
        op.execute(
            'INSERT INTO users (id, email, username, password_hash, created_at) '
            'SELECT id, email, username, "passwordHash", "createdAt" FROM "User"'
        )
        op.execute("SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users))")
    for old_table in ("SortingSession", "User", "_prisma_migrations"):
        if old_table in tables:
            op.drop_table(old_table)


def downgrade():
    op.drop_table("quiz_attempts")
    op.drop_table("problem_progress")
    op.drop_table("topic_progress")
    op.drop_table("users")
