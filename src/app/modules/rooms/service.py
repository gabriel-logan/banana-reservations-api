from app.modules.rooms.repository import RoomRepository
from app.modules.rooms.schemas import RoomCreate, RoomResponse


class RoomService:
    def __init__(self, repo: RoomRepository):
        self.repo = repo

    def list_rooms(self, branch_id: int | None = None) -> list[RoomResponse]:
        raise NotImplementedError

    def get_room(self, room_id: int) -> RoomResponse:
        raise NotImplementedError

    def create_room(self, data: RoomCreate) -> RoomResponse:
        raise NotImplementedError

    def delete_room(self, room_id: int) -> None:
        raise NotImplementedError
