from datetime import datetime
import logging

from app.modules.reservations.entity import Reservation
from sqlalchemy.orm import Session
from app.modules.rooms.entity import Room
from app.modules.rooms.schemas import RoomCreate

logger = logging.getLogger(__name__)


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, branch_id: int | None = None) -> list[Room]:
        query = self.db.query(Room)
        if branch_id is not None:
            query = query.filter(Room.branch_id == branch_id)
        return query.order_by(Room.name.asc()).all()

    def get_available(
        self,
        branch_id: int | None,
        start_time: datetime,
        end_time: datetime,
        ignore_reservation_id: int | None = None,
    ) -> list[Room]:
        conflict_query = self.db.query(Reservation.id).filter(
            Reservation.room_id == Room.id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
        )

        if ignore_reservation_id is not None:
            conflict_query = conflict_query.filter(
                Reservation.id != ignore_reservation_id
            )

        query = self.db.query(Room).filter(~conflict_query.exists())

        if branch_id is not None:
            query = query.filter(Room.branch_id == branch_id)

        rooms = query.order_by(Room.name.asc()).all()

        logger.debug(
            "Fetched %s available rooms for branch_id=%s between %s and %s (ignore_reservation_id=%s).",
            len(rooms),
            branch_id,
            start_time.isoformat(),
            end_time.isoformat(),
            ignore_reservation_id,
        )

        return rooms

    def get_by_id(self, room_id: int) -> Room | None:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def create(self, data: RoomCreate) -> Room:
        room = Room(name=data.name, branch_id=data.branch_id)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def has_reservations(self, room_id: int) -> bool:
        return self.db.query(Reservation.id).filter(Reservation.room_id == room_id).first() is not None

    def delete(self, room_id: int) -> None:
        room = self.get_by_id(room_id)
        if room is not None:
            self.db.delete(room)
            self.db.commit()
