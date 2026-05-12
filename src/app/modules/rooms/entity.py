from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from app.infrastructure.database.base import Base


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
