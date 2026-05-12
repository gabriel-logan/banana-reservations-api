from app.modules.rooms.entity import Room
from sqlalchemy.orm import Session
from app.modules.branches.entity import Branch
from app.modules.branches.schemas import BranchCreate


class BranchRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Branch]:
        return self.db.query(Branch).order_by(Branch.name.asc()).all()

    def get_by_id(self, branch_id: int) -> Branch | None:
        return self.db.query(Branch).filter(Branch.id == branch_id).first()

    def create(self, data: BranchCreate) -> Branch:
        branch = Branch(name=data.name)
        self.db.add(branch)
        self.db.commit()
        self.db.refresh(branch)
        return branch

    def has_rooms(self, branch_id: int) -> bool:
        return self.db.query(Room.id).filter(Room.branch_id == branch_id).first() is not None

    def delete(self, branch_id: int) -> None:
        branch = self.get_by_id(branch_id)
        if branch is not None:
            self.db.delete(branch)
            self.db.commit()
