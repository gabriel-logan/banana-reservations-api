from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.common.responses import to_camel


class BranchBase(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str


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
