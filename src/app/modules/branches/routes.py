from datetime import datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.infrastructure.database.session import get_db
from app.modules.branches.schemas import BranchCreate, BranchResponse
from app.infrastructure.security.jwt_auth import get_current_user
from app.modules.branches.repository import BranchRepository
from app.modules.branches.service import BranchService

router = APIRouter(prefix="/branches", tags=["branches"])


def get_branch_service(db: Session = Depends(get_db)) -> BranchService:
    return BranchService(BranchRepository(db))


@router.get("", response_model=list[BranchResponse], response_model_by_alias=True)
def list_branches(
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    ignore_reservation_id: int | None = None,
    service: BranchService = Depends(get_branch_service),
    _=Depends(get_current_user),
):
    return service.list_branches(start_time, end_time, ignore_reservation_id)


@router.get("/{branch_id}", response_model=BranchResponse, response_model_by_alias=True)
def get_branch(
    branch_id: int,
    service: BranchService = Depends(get_branch_service),
    _=Depends(get_current_user),
):
    return service.get_branch(branch_id)


@router.post("", response_model=BranchResponse, response_model_by_alias=True, status_code=201)
def create_branch(
    data: BranchCreate,
    service: BranchService = Depends(get_branch_service),
    _=Depends(get_current_user),
):
    return service.create_branch(data)


@router.delete("/{branch_id}", status_code=204)
def delete_branch(
    branch_id: int,
    service: BranchService = Depends(get_branch_service),
    _=Depends(get_current_user),
):
    service.delete_branch(branch_id)
    return Response(status_code=204)
