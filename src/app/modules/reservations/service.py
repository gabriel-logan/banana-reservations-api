from app.modules.reservations.entity import Reservation
from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.reservations.repository import ReservationRepository
from app.modules.reservations.schemas import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from app.modules.rooms.repository import RoomRepository


class ReservationService:
    def __init__(
        self,
        repo: ReservationRepository,
        room_repo: RoomRepository,
        branch_repo: BranchRepository,
    ):
        self.repo = repo
        self.room_repo = room_repo
        self.branch_repo = branch_repo

    def list_reservations(self, room_id: int | None = None) -> list[ReservationResponse]:
        return [self._to_response(reservation) for reservation in self.repo.get_all(room_id)]

    def get_reservation(self, reservation_id: int) -> ReservationResponse:
        reservation = self.repo.get_by_id(reservation_id)
        if reservation is None:
            raise NotFoundException("Reservation not found.")
        return self._to_response(reservation)

    def create_reservation(self, data: ReservationCreate) -> ReservationResponse:
        room = self._validate_room_and_branch(data.branch_id, data.room_id)
        if self.repo.has_conflict(room.id, data.start_time, data.end_time):
            raise ConflictException(
                "There is already a reservation for this room in the selected time range."
            )
        reservation = self.repo.create(data)
        return self._to_response(reservation)

    def update_reservation(self, reservation_id: int, data: ReservationUpdate) -> ReservationResponse:
        reservation = self.repo.get_by_id(reservation_id)
        if reservation is None:
            raise NotFoundException("Reservation not found.")

        room = self._validate_room_and_branch(data.branch_id, data.room_id)
        if self.repo.has_conflict(
            room.id,
            data.start_time,
            data.end_time,
            ignore_reservation_id=reservation_id,
        ):
            raise ConflictException(
                "There is already a reservation for this room in the selected time range."
            )

        updated_reservation = self.repo.update(reservation, data)
        return self._to_response(updated_reservation)

    def delete_reservation(self, reservation_id: int) -> None:
        reservation = self.repo.get_by_id(reservation_id)
        if reservation is None:
            raise NotFoundException("Reservation not found.")
        self.repo.delete(reservation_id)

    def _validate_room_and_branch(self, branch_id: int, room_id: int):
        branch = self.branch_repo.get_by_id(branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")

        room = self.room_repo.get_by_id(room_id)
        if room is None:
            raise NotFoundException("Room not found.")

        if room.branch_id != branch_id:
            raise ConflictException("Selected room does not belong to the selected branch.")

        return room

    @staticmethod
    def _to_response(reservation: Reservation) -> ReservationResponse:
        return ReservationResponse(
            id=reservation.id,
            branch_id=reservation.room.branch.id,
            branch_name=reservation.room.branch.name,
            room_id=reservation.room.id,
            room_name=reservation.room.name,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            responsible=reservation.responsible,
            coffee=reservation.coffee,
            people_quantity=reservation.people_quantity,
            description=reservation.description,
            created_at=reservation.created_at,
        )
