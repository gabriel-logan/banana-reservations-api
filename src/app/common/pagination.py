from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    size: int
