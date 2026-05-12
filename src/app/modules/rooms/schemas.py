from datetime import datetime
from pydantic import BaseModel


class RoomBase(BaseModel):
    name: str
    branch_id: int


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
