from datetime import datetime
import logging

from app.modules.reservations.entity import Reservation
from app.modules.rooms.entity import Room
from sqlalchemy.orm import Session
from app.modules.branches.entity import Branch
from app.modules.branches.schemas import BranchCreate

logger = logging.getLogger(__name__)


class BranchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Branch]:
        return self.db.query(Branch).order_by(Branch.name.asc()).all()

    def get_available(
        self,
        start_time: datetime,
        end_time: datetime,
        ignore_reservation_id: int | None = None,
    ) -> list[Branch]:
        conflict_query = self.db.query(Reservation.id).filter(
            Reservation.room_id == Room.id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
        )

        if ignore_reservation_id is not None:
            conflict_query = conflict_query.filter(
                Reservation.id != ignore_reservation_id
            )

        branches = (
            self.db.query(Branch)
            .join(Room, Room.branch_id == Branch.id)
            .filter(~conflict_query.exists())
            .distinct()
            .order_by(Branch.name.asc())
            .all()
        )

        logger.debug(
            "Fetched %s available branches between %s and %s (ignore_reservation_id=%s).",
            len(branches),
            start_time.isoformat(),
            end_time.isoformat(),
            ignore_reservation_id,
        )

        return branches

    def get_by_id(self, branch_id: int) -> Branch | None:
        return self.db.query(Branch).filter(Branch.id == branch_id).first()

    def create(self, data: BranchCreate) -> Branch:
        branch = Branch(name=data.name)
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def has_rooms(self, branch_id: int) -> bool:
        return self.db.query(Room.id).filter(Room.branch_id == branch_id).first() is not None

    def delete(self, branch_id: int) -> None:
        branch = self.get_by_id(branch_id)
        if branch is not None:
            self.db.delete(branch)
            self.db.commit()
