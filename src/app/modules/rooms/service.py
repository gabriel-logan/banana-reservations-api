from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.rooms.repository import RoomRepository
from app.modules.rooms.schemas import RoomCreate, RoomResponse


class RoomService:
    def __init__(self, repo: RoomRepository, branch_repo: BranchRepository):
        self.repo = repo
        self.branch_repo = branch_repo

    def list_rooms(self, branch_id: int | None = None) -> list[RoomResponse]:
        return [RoomResponse.model_validate(room) for room in self.repo.get_all(branch_id)]

    def get_room(self, room_id: int) -> RoomResponse:
        room = self.repo.get_by_id(room_id)
        if room is None:
            raise NotFoundException("Room not found.")
        return RoomResponse.model_validate(room)

    def create_room(self, data: RoomCreate) -> RoomResponse:
        branch = self.branch_repo.get_by_id(data.branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        return RoomResponse.model_validate(self.repo.create(data))

    def delete_room(self, room_id: int) -> None:
        room = self.repo.get_by_id(room_id)
        if room is None:
            raise NotFoundException("Room not found.")
        if self.repo.has_reservations(room_id):
            raise ConflictException("Cannot delete room with reservations linked to it.")
        self.repo.delete(room_id)
