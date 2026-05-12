from sqlalchemy.orm import Session
from app.modules.reservations.entity import Reservation
from app.modules.reservations.schemas import ReservationCreate


class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, room_id: int | None = None) -> list[Reservation]:
        raise NotImplementedError

    def get_by_id(self, reservation_id: int) -> Reservation | None:
        raise NotImplementedError

    def create(self, data: ReservationCreate) -> Reservation:
        raise NotImplementedError

    def delete(self, reservation_id: int) -> None:
        raise NotImplementedError
