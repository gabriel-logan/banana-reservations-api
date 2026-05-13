from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.infrastructure.security.jwt_auth import get_current_user
from app.modules.branches.repository import BranchRepository
from app.modules.reservations.repository import ReservationRepository
from app.modules.reservations.schemas import (
    ReservationBulkDeleteRequest,
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from app.modules.reservations.service import ReservationService
from app.modules.rooms.repository import RoomRepository

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: Session = Depends(get_db)) -> ReservationService:
    return ReservationService(
        ReservationRepository(db),
        RoomRepository(db),
        BranchRepository(db),
    )


@router.get("", response_model=list[ReservationResponse], response_model_by_alias=True)
def list_reservations(
    room_id: int | None = None,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    return service.list_reservations(room_id)


@router.get("/{reservation_id}", response_model=ReservationResponse, response_model_by_alias=True)
def get_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    return service.get_reservation(reservation_id)


@router.post("", response_model=ReservationResponse, response_model_by_alias=True, status_code=201)
def create_reservation(
    data: ReservationCreate,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    return service.create_reservation(data)


@router.put("/{reservation_id}", response_model=ReservationResponse, response_model_by_alias=True)
def update_reservation(
    reservation_id: int,
    data: ReservationUpdate,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    return service.update_reservation(reservation_id, data)


@router.delete("/{reservation_id}", status_code=204)
def delete_reservation(
    reservation_id: int,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    service.delete_reservation(reservation_id)
    return Response(status_code=204)


@router.post("/bulk-delete", status_code=204)
def bulk_delete_reservations(
    data: ReservationBulkDeleteRequest,
    service: ReservationService = Depends(get_reservation_service),
    _=Depends(get_current_user),
):
    service.delete_reservations(data)
    return Response(status_code=204)
