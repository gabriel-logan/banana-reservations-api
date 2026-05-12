from datetime import datetime
from pydantic import BaseModel


class ReservationBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    responsible: str
    coffee: bool = False
    people_quantity: int | None = None
    description: str | None = None


class ReservationCreate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
