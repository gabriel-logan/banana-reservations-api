from sqlalchemy.orm import Session
from app.modules.rooms.entity import Room
from app.modules.rooms.schemas import RoomCreate


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, branch_id: int | None = None) -> list[Room]:
        raise NotImplementedError

    def get_by_id(self, room_id: int) -> Room | None:
        raise NotImplementedError

    def create(self, data: RoomCreate) -> Room:
        raise NotImplementedError

    def delete(self, room_id: int) -> None:
        raise NotImplementedError
