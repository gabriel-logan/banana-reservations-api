from fastapi import APIRouter, Depends
from app.modules.rooms.schemas import RoomCreate, RoomResponse
from app.infrastructure.security.jwt_auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("/", response_model=list[RoomResponse])
def list_rooms(branch_id: int | None = None, _=Depends(get_current_user)):
    raise NotImplementedError


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, _=Depends(get_current_user)):
    raise NotImplementedError


@router.post("/", response_model=RoomResponse, status_code=201)
def create_room(data: RoomCreate, _=Depends(get_current_user)):
    raise NotImplementedError


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, _=Depends(get_current_user)):
    raise NotImplementedError
