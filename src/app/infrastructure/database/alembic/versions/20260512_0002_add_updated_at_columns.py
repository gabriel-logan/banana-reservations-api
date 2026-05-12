"""add updated_at columns

Revision ID: 20260512_0002
Revises: 20260512_0001
Create Date: 2026-05-12 00:10:00
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260512_0002"
down_revision: Union[str, Sequence[str], None] = "20260512_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE branches
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NULL;
        """
    )
    op.execute(
        """
        UPDATE branches
        SET updated_at = COALESCE(updated_at, created_at, NOW())
        WHERE updated_at IS NULL;
        """
    )
    op.execute(
        """
        ALTER TABLE branches
        ALTER COLUMN updated_at SET DEFAULT NOW();
        """
    )
    op.execute(
        """
        ALTER TABLE branches
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )

    op.execute(
        """
        ALTER TABLE rooms
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NULL;
        """
    )
    op.execute(
        """
        UPDATE rooms
        SET updated_at = COALESCE(updated_at, created_at, NOW())
        WHERE updated_at IS NULL;
        """
    )
    op.execute(
        """
        ALTER TABLE rooms
        ALTER COLUMN updated_at SET DEFAULT NOW();
        """
    )
    op.execute(
        """
        ALTER TABLE rooms
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )

    op.execute(
        """
        ALTER TABLE reservations
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NULL;
        """
    )
    op.execute(
        """
        UPDATE reservations
        SET updated_at = COALESCE(updated_at, created_at, NOW())
        WHERE updated_at IS NULL;
        """
    )
    op.execute(
        """
        ALTER TABLE reservations
        ALTER COLUMN updated_at SET DEFAULT NOW();
        """
    )
    op.execute(
        """
        ALTER TABLE reservations
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE reservations
        DROP COLUMN IF EXISTS updated_at;
        """
    )
    op.execute(
        """
        ALTER TABLE rooms
        DROP COLUMN IF EXISTS updated_at;
        """
    )
    op.execute(
        """
        ALTER TABLE branches
        DROP COLUMN IF EXISTS updated_at;
        """
    )
