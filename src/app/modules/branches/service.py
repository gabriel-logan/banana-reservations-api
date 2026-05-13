from datetime import datetime
import logging

from app.common.exceptions import ConflictException, NotFoundException
from app.modules.branches.repository import BranchRepository
from app.modules.branches.schemas import BranchCreate, BranchResponse

logger = logging.getLogger(__name__)


class BranchService:
    def __init__(self, repo: BranchRepository):
        self.repo = repo

    def list_branches(
        self,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        ignore_reservation_id: int | None = None,
    ) -> list[BranchResponse]:
        if start_time and end_time:
            branches = self.repo.get_available(
                start_time,
                end_time,
                ignore_reservation_id,
            )
            logger.info(
                "Listed available branches between %s and %s. count=%s",
                start_time.isoformat(),
                end_time.isoformat(),
                len(branches),
            )
        else:
            branches = self.repo.get_all()
            logger.debug("Listed all branches. count=%s", len(branches))

        return [BranchResponse.model_validate(branch) for branch in branches]

    def get_branch(self, branch_id: int) -> BranchResponse:
        branch = self.repo.get_by_id(branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        return BranchResponse.model_validate(branch)

    def create_branch(self, data: BranchCreate) -> BranchResponse:
        logger.info("Creating branch with name=%s", data.name)
        return BranchResponse.model_validate(self.repo.create(data))

    def delete_branch(self, branch_id: int) -> None:
        branch = self.repo.get_by_id(branch_id)
        if branch is None:
            raise NotFoundException("Branch not found.")
        if self.repo.has_rooms(branch_id):
            logger.warning(
                "Cannot delete branch id=%s because it still has linked rooms.",
                branch_id,
            )
            raise ConflictException("Cannot delete branch with rooms linked to it.")
        logger.info("Deleting branch id=%s", branch_id)
        self.repo.delete(branch_id)
