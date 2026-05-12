from sqlalchemy.orm import Session
from app.modules.rooms.entity import Room
from app.modules.rooms.schemas import RoomCreate


class RoomRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, branch_id: int | None = None) -> list[Room]:
        query = self.db.query(Room)
        if branch_id is not None:
            query = query.filter(Room.branch_id == branch_id)
        return query.order_by(Room.name.asc()).all()

    def get_by_id(self, room_id: int) -> Room | None:
        return self.db.query(Room).filter(Room.id == room_id).first()

    def create(self, data: RoomCreate) -> Room:
        room = Room(name=data.name, branch_id=data.branch_id)
        self.db.add(room)
        self.db.commit()
        self.db.refresh(room)
        return room

    def delete(self, room_id: int) -> None:
        room = self.get_by_id(room_id)
        if room is not None:
            self.db.delete(room)
            self.db.commit()
