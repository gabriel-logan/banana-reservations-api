from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.branches.schemas import BranchCreate, BranchResponse


class BranchService:
    def __init__(self, repo: BranchRepository):
        self.repo = repo

    def list_branches(self) -> list[BranchResponse]:
        return [BranchResponse.model_validate(branch) for branch in self.repo.get_all()]

    def get_branch(self, branch_id: int) -> BranchResponse:
        branch = self.repo.get_by_id(branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        return BranchResponse.model_validate(branch)

    def create_branch(self, data: BranchCreate) -> BranchResponse:
        return BranchResponse.model_validate(self.repo.create(data))

    def delete_branch(self, branch_id: int) -> None:
        branch = self.repo.get_by_id(branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        if self.repo.has_rooms(branch_id):
            raise ConflictException("Cannot delete branch with rooms linked to it.")
        self.repo.delete(branch_id)
