from fastapi import APIRouter, Depends
from app.modules.branches.schemas import BranchCreate, BranchResponse
from app.infrastructure.security.jwt_auth import get_current_user

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("/", response_model=list[BranchResponse])
def list_branches(_=Depends(get_current_user)):
    raise NotImplementedError


@router.get("/{branch_id}", response_model=BranchResponse)
def get_branch(branch_id: int, _=Depends(get_current_user)):
    raise NotImplementedError


@router.post("/", response_model=BranchResponse, status_code=201)
def create_branch(data: BranchCreate, _=Depends(get_current_user)):
    raise NotImplementedError


@router.delete("/{branch_id}", status_code=204)
def delete_branch(branch_id: int, _=Depends(get_current_user)):
    raise NotImplementedError
