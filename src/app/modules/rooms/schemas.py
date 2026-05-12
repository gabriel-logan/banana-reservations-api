from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.common.responses import to_camel


class RoomBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    branch_id: int


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
