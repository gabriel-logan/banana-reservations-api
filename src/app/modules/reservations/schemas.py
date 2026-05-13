from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.common.responses import to_camel


class ReservationBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    branch_id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    responsible: str = Field(min_length=1, max_length=255)
    coffee: bool = False
    people_quantity: int | None = Field(default=None, gt=0)
    description: str | None = None

    @model_validator(mode="after")
    def validate_fields(self):
        self.responsible = self.responsible.strip()
        self.description = self.description.strip() if self.description else None

        if not self.responsible:
            raise ValueError("Responsible is required.")

        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time.")

        if self.coffee and self.people_quantity is None:
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
