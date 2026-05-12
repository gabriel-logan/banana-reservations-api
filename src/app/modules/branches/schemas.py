from datetime import datetime
from pydantic import BaseModel


class BranchBase(BaseModel):
    name: str


class BranchCreate(BranchBase):
    pass


class BranchResponse(BranchBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
