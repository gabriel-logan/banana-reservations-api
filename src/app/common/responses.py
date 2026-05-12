from pydantic import BaseModel


class ErrorResponse(BaseModel):
    message: str
    status_code: int
