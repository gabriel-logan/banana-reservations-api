"""add reservation user_id

Revision ID: 20260513_0003
Revises: 20260512_0002
Create Date: 2026-05-13 17:00:00
"""

from alembic import op


revision = "20260513_0003"
down_revision = "20260512_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE reservations ADD COLUMN IF NOT EXISTS user_id VARCHAR(36)")
    op.execute(
        """
        UPDATE reservations
        SET user_id = '11111111-1111-1111-1111-111111111111'
        WHERE user_id IS NULL
        """
    )
    op.execute("ALTER TABLE reservations ALTER COLUMN user_id SET NOT NULL")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_reservations_user_id ON reservations (user_id)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_reservations_user_id")
    op.execute("ALTER TABLE reservations DROP COLUMN IF EXISTS user_id")
