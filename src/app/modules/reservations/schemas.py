from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

from app.common.responses import to_camel


class ReservationBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    branch_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    responsible: str
    coffee: bool = False
    people_quantity: int | None = None
    description: str | None = None

    @model_validator(mode="after")
    def validate_fields(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time.")

        if self.coffee and (self.people_quantity is None or self.people_quantity <= 0):
            raise ValueError("People quantity is required when coffee is selected.")

        if not self.coffee:
            self.people_quantity = None

        return self


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(ReservationBase):
    pass


class ReservationResponse(ReservationBase):
    id: int
    branch_name: str
    room_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
