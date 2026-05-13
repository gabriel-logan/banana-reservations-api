import logging

from app.modules.reservations.entity import Reservation
from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.reservations.repository import ReservationRepository
from app.modules.reservations.schemas import (
    ReservationBulkDeleteRequest,
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from app.modules.rooms.repository import RoomRepository

logger = logging.getLogger(__name__)


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

    def list_reservations(self, user_id: str, room_id: int | None = None) -> list[ReservationResponse]:
        reservations = self.repo.get_all(user_id, room_id)
        logger.info(
            "Listed reservations for user_id=%s with room_id=%s. count=%s",
            user_id,
            room_id,
            len(reservations),
        )
        return [self._to_response(reservation) for reservation in reservations]

    def get_reservation(self, user_id: str, reservation_id: int) -> ReservationResponse:
        logger.debug("Fetching reservation id=%s for user_id=%s", reservation_id, user_id)
        reservation = self.repo.get_by_id(reservation_id, user_id)
        if reservation is None:
            logger.warning("Reservation id=%s not found for user_id=%s.", reservation_id, user_id)
            raise NotFoundException("Reservation not found.")
        return self._to_response(reservation)

    def create_reservation(self, user_id: str, data: ReservationCreate) -> ReservationResponse:
        logger.info(
            "Creating reservation for user_id=%s with branch_id=%s room_id=%s start=%s end=%s coffee=%s people_quantity=%s",
            user_id,
            data.branch_id,
            data.room_id,
            data.start_time.isoformat(),
            data.end_time.isoformat(),
            data.coffee,
            data.people_quantity,
        )
        room = self._validate_room_and_branch(data.branch_id, data.room_id)
        if self.repo.has_conflict(room.id, data.start_time, data.end_time):
            logger.warning(
                "Reservation conflict detected on create for room_id=%s between %s and %s.",
                room.id,
                data.start_time.isoformat(),
                data.end_time.isoformat(),
            )
            raise ConflictException(
                "There is already a reservation for this room in the selected time range."
            )
        reservation = self.repo.create(user_id, data)
        logger.info("Reservation created successfully. id=%s", reservation.id)
        return self._to_response(reservation)

    def update_reservation(self, user_id: str, reservation_id: int, data: ReservationUpdate) -> ReservationResponse:
        logger.info(
            "Updating reservation id=%s for user_id=%s with branch_id=%s room_id=%s start=%s end=%s coffee=%s people_quantity=%s",
            reservation_id,
            user_id,
            data.branch_id,
            data.room_id,
            data.start_time.isoformat(),
            data.end_time.isoformat(),
            data.coffee,
            data.people_quantity,
        )
        reservation = self.repo.get_by_id(reservation_id, user_id)
        if reservation is None:
            logger.warning("Reservation id=%s not found for update by user_id=%s.", reservation_id, user_id)
            raise NotFoundException("Reservation not found.")

        room = self._validate_room_and_branch(data.branch_id, data.room_id)
        if self.repo.has_conflict(
            room.id,
            data.start_time,
            data.end_time,
            ignore_reservation_id=reservation_id,
        ):
            logger.warning(
                "Reservation conflict detected on update for reservation_id=%s room_id=%s between %s and %s.",
                reservation_id,
                room.id,
                data.start_time.isoformat(),
                data.end_time.isoformat(),
            )
            raise ConflictException(
                "There is already a reservation for this room in the selected time range."
            )

        updated_reservation = self.repo.update(reservation, data)
        logger.info("Reservation updated successfully. id=%s", updated_reservation.id)
        return self._to_response(updated_reservation)

    def delete_reservation(self, user_id: str, reservation_id: int) -> None:
        logger.info("Deleting reservation id=%s for user_id=%s", reservation_id, user_id)
        reservation = self.repo.get_by_id(reservation_id, user_id)
        if reservation is None:
            logger.warning("Reservation id=%s not found for delete by user_id=%s.", reservation_id, user_id)
            raise NotFoundException("Reservation not found.")
        self.repo.delete(reservation_id, user_id)

    def delete_reservations(self, user_id: str, data: ReservationBulkDeleteRequest) -> None:
        logger.info("Bulk deleting reservations for user_id=%s ids=%s", user_id, data.reservation_ids)
        reservations = self.repo.get_by_ids(user_id, data.reservation_ids)

        if len(reservations) != len(data.reservation_ids):
            logger.warning(
                "Bulk delete failed for user_id=%s because some reservations were not found. requested_ids=%s found=%s",
                user_id,
                data.reservation_ids,
                len(reservations),
            )
            raise NotFoundException("One or more reservations were not found.")

        self.repo.delete_many(reservations)

    def _validate_room_and_branch(self, branch_id: int, room_id: int):
        branch = self.branch_repo.get_by_id(branch_id)
        if branch is None:
            logger.warning("Branch id=%s not found while validating reservation.", branch_id)
            raise NotFoundException("Branch not found.")

        room = self.room_repo.get_by_id(room_id)
        if room is None:
            logger.warning("Room id=%s not found while validating reservation.", room_id)
            raise NotFoundException("Room not found.")

        if room.branch_id != branch_id:
            logger.warning(
                "Room id=%s does not belong to branch_id=%s.",
                room_id,
                branch_id,
            )
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
            updated_at=reservation.updated_at,
        )
