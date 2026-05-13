from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.common.responses import to_camel


class BranchBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str = Field(min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_name(self):
        self.name = self.name.strip()

        if not self.name:
            raise ValueError("Name is required.")

        return self


class BranchCreate(BranchBase):
    pass


class BranchResponse(BranchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )
