from app.modules.branches.repository import BranchRepository
from app.modules.branches.schemas import BranchCreate, BranchResponse


class BranchService:
    def __init__(self, repo: BranchRepository):
        self.repo = repo

    def list_branches(self) -> list[BranchResponse]:
        raise NotImplementedError

    def get_branch(self, branch_id: int) -> BranchResponse:
        raise NotImplementedError

    def create_branch(self, data: BranchCreate) -> BranchResponse:
        raise NotImplementedError

    def delete_branch(self, branch_id: int) -> None:
        raise NotImplementedError
