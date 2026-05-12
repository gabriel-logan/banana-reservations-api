from app.modules.reservations.repository import ReservationRepository
from app.modules.reservations.schemas import ReservationCreate, ReservationResponse


class ReservationService:
    def __init__(self, repo: ReservationRepository):
        self.repo = repo

    def list_reservations(self, room_id: int | None = None) -> list[ReservationResponse]:
        raise NotImplementedError

    def get_reservation(self, reservation_id: int) -> ReservationResponse:
        raise NotImplementedError

    def create_reservation(self, data: ReservationCreate) -> ReservationResponse:
        raise NotImplementedError

    def delete_reservation(self, reservation_id: int) -> None:
        raise NotImplementedError
