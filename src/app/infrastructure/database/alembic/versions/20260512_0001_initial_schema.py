"""initial schema

Revision ID: 20260512_0001
Revises:
Create Date: 2026-05-12 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260512_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS branches (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
    )
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
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_branches_id ON branches (id);")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            branch_id INTEGER NOT NULL REFERENCES branches(id),
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
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
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_rooms_id ON rooms (id);")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS reservations (
            id SERIAL PRIMARY KEY,
            room_id INTEGER NOT NULL REFERENCES rooms(id),
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            responsible VARCHAR(255) NOT NULL,
            coffee BOOLEAN NOT NULL DEFAULT FALSE,
            people_quantity INTEGER NULL,
            description TEXT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
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
        ALTER COLUMN updated_at SET NOT NULL;
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_reservations_id ON reservations (id);")


def downgrade() -> None:
    op.drop_index("ix_reservations_id", table_name="reservations")
    op.drop_table("reservations")
    op.drop_index("ix_rooms_id", table_name="rooms")
    op.drop_table("rooms")
    op.drop_index("ix_branches_id", table_name="branches")
    op.drop_table("branches")
