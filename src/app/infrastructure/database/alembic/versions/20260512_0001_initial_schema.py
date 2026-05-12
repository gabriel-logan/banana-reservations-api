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
    op.create_table(
        "branches",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_branches_id", "branches", ["id"], unique=False)

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("branch_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"]),
    )
    op.create_index("ix_rooms_id", "rooms", ["id"], unique=False)

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("responsible", sa.String(length=255), nullable=False),
        sa.Column("coffee", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("people_quantity", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
    )
    op.create_index("ix_reservations_id", "reservations", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_reservations_id", table_name="reservations")
    op.drop_table("reservations")
    op.drop_index("ix_rooms_id", table_name="rooms")
    op.drop_table("rooms")
    op.drop_index("ix_branches_id", table_name="branches")
    op.drop_table("branches")
