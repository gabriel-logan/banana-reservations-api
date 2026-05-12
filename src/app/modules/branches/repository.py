from sqlalchemy.orm import Session
from app.modules.branches.entity import Branch
from app.modules.branches.schemas import BranchCreate


class BranchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Branch]:
        raise NotImplementedError

    def get_by_id(self, branch_id: int) -> Branch | None:
        raise NotImplementedError

    def create(self, data: BranchCreate) -> Branch:
        raise NotImplementedError

    def delete(self, branch_id: int) -> None:
        raise NotImplementedError
