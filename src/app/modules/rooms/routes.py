from datetime import datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.modules.rooms.schemas import RoomCreate, RoomResponse
from app.infrastructure.security.jwt_auth import get_current_user
from app.modules.branches.repository import BranchRepository
from app.modules.rooms.repository import RoomRepository
from app.modules.rooms.service import RoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


def get_room_service(db: Session = Depends(get_db)) -> RoomService:
    return RoomService(RoomRepository(db), BranchRepository(db))


@router.get("", response_model=list[RoomResponse], response_model_by_alias=True)
def list_rooms(
    branch_id: int | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    ignore_reservation_id: int | None = None,
    service: RoomService = Depends(get_room_service),
    _=Depends(get_current_user),
):
    return service.list_rooms(
        branch_id,
        start_time,
        end_time,
        ignore_reservation_id,
    )


@router.get("/{room_id}", response_model=RoomResponse, response_model_by_alias=True)
def get_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    _=Depends(get_current_user),
):
    return service.get_room(room_id)


@router.post("", response_model=RoomResponse, response_model_by_alias=True, status_code=201)
def create_room(
    data: RoomCreate,
    service: RoomService = Depends(get_room_service),
    _=Depends(get_current_user),
):
    return service.create_room(data)


@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    _=Depends(get_current_user),
):
    service.delete_room(room_id)
    return Response(status_code=204)
