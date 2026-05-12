from fastapi import APIRouter, Depends
from app.modules.reservations.schemas import ReservationCreate, ReservationResponse
from app.infrastructure.security.jwt_auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.get("/", response_model=list[ReservationResponse])
def list_reservations(room_id: int | None = None, _=Depends(get_current_user)):
    raise NotImplementedError


@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(reservation_id: int, _=Depends(get_current_user)):
    raise NotImplementedError


@router.post("/", response_model=ReservationResponse, status_code=201)
def create_reservation(data: ReservationCreate, _=Depends(get_current_user)):
    raise NotImplementedError


@router.delete("/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: int, _=Depends(get_current_user)):
    raise NotImplementedError
