from sqlalchemy.orm import Session

from app.modules.branches.entity import Branch
from app.modules.reservations.entity import Reservation
from app.modules.reservations.schemas import ReservationCreate, ReservationUpdate
from app.modules.rooms.entity import Room


class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, room_id: int | None = None) -> list[Reservation]:
        query = self.db.query(Reservation).join(Room).join(Branch)
        if room_id is not None:
            query = query.filter(Reservation.room_id == room_id)
        return query.order_by(Reservation.start_time.asc()).all()

    def get_by_id(self, reservation_id: int) -> Reservation | None:
        return (
            self.db.query(Reservation)
            .join(Room)
            .join(Branch)
            .filter(Reservation.id == reservation_id)
            .first()
        )

    def create(self, data: ReservationCreate) -> Reservation:
        reservation = Reservation(
            room_id=data.room_id,
            start_time=data.start_time,
            end_time=data.end_time,
            responsible=data.responsible,
            coffee=data.coffee,
            people_quantity=data.people_quantity,
            description=data.description,
        )
        self.db.add(reservation)
        self.db.commit()
        return self.get_by_id(reservation.id)

    def update(self, reservation: Reservation, data: ReservationUpdate) -> Reservation:
        reservation.room_id = data.room_id
        reservation.start_time = data.start_time
        reservation.end_time = data.end_time
        reservation.responsible = data.responsible
        reservation.coffee = data.coffee
        reservation.people_quantity = data.people_quantity
        reservation.description = data.description
        self.db.commit()
        return self.get_by_id(reservation.id)

    def delete(self, reservation_id: int) -> None:
        reservation = self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
        if reservation is not None:
            self.db.delete(reservation)
            self.db.commit()

    def get_by_ids(self, reservation_ids: list[int]) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.id.in_(reservation_ids))
            .all()
        )

    def delete_many(self, reservations: list[Reservation]) -> None:
        for reservation in reservations:
            self.db.delete(reservation)
        self.db.commit()

    def has_conflict(
        self,
        room_id: int,
        start_time,
        end_time,
        ignore_reservation_id: int | None = None,
    ) -> bool:
        query = self.db.query(Reservation).filter(
            Reservation.room_id == room_id,
            Reservation.start_time < end_time,
            Reservation.end_time > start_time,
        )

        if ignore_reservation_id is not None:
            query = query.filter(Reservation.id != ignore_reservation_id)

        return self.db.query(query.exists()).scalar()
