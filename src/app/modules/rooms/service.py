from datetime import datetime
import logging

from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.rooms.repository import RoomRepository
from app.modules.rooms.schemas import RoomCreate, RoomResponse

logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, repo: RoomRepository, branch_repo: BranchRepository):
        self.repo = repo
        self.branch_repo = branch_repo

    def list_rooms(
        self,
        branch_id: int | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ignore_reservation_id: int | None = None,
    ) -> list[RoomResponse]:
        if start_time and end_time:
            rooms = self.repo.get_available(
                branch_id,
                start_time,
                end_time,
                ignore_reservation_id,
            )
            logger.info(
                "Listed available rooms for branch_id=%s between %s and %s. count=%s",
                branch_id,
                start_time.isoformat(),
                end_time.isoformat(),
                len(rooms),
            )
        else:
            rooms = self.repo.get_all(branch_id)
            logger.debug(
                "Listed rooms for branch_id=%s without availability filter. count=%s",
                branch_id,
                len(rooms),
            )

        return [RoomResponse.model_validate(room) for room in rooms]

    def get_room(self, room_id: int) -> RoomResponse:
        room = self.repo.get_by_id(room_id)
        if room is None:
            raise NotFoundException("Room not found.")
        return RoomResponse.model_validate(room)

    def create_room(self, data: RoomCreate) -> RoomResponse:
        branch = self.branch_repo.get_by_id(data.branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        logger.info("Creating room name=%s for branch_id=%s", data.name, data.branch_id)
        return RoomResponse.model_validate(self.repo.create(data))

    def delete_room(self, room_id: int) -> None:
        room = self.repo.get_by_id(room_id)
        if room is None:
            raise NotFoundException("Room not found.")
        if self.repo.has_reservations(room_id):
            logger.warning(
                "Cannot delete room id=%s because it still has linked reservations.",
                room_id,
            )
            raise ConflictException("Cannot delete room with reservations linked to it.")
        logger.info("Deleting room id=%s", room_id)
        self.repo.delete(room_id)
