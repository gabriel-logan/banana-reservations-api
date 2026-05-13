from datetime import UTC, datetime, timedelta
import logging

from sqlalchemy.orm import Session

from app.modules.branches.entity import Branch
from app.modules.reservations.entity import Reservation
from app.modules.rooms.entity import Room

logger = logging.getLogger(__name__)


def seed_initial_data(db: Session) -> None:
    if db.query(Branch.id).count() > 0:
        logger.debug("Skipping reservations seed because branches already exist.")
        return

    logger.info("Seeding initial branches, rooms, and reservations.")

    branches = [
        Branch(name="Sao Paulo - Paulista"),
        Branch(name="Sao Paulo - Vila Olimpia"),
        Branch(name="Rio de Janeiro - Botafogo"),
        Branch(name="Campinas - Taquaral"),
    ]

    db.add_all(branches)
    db.flush()

    rooms = [
        Room(name="Aroeira", branch_id=branches[0].id),
        Room(name="Bromelia", branch_id=branches[0].id),
        Room(name="Caju", branch_id=branches[1].id),
        Room(name="Dende", branch_id=branches[1].id),
        Room(name="Ipe", branch_id=branches[2].id),
        Room(name="Jatoba", branch_id=branches[2].id),
        Room(name="Jabuticaba", branch_id=branches[3].id),
    ]

    db.add_all(rooms)
    db.flush()

    tomorrow = datetime.now(UTC).replace(
        hour=9,
        minute=0,
        second=0,
        microsecond=0,
    ) + timedelta(days=1)

    reservations = [
        Reservation(
            room_id=rooms[0].id,
            start_time=tomorrow,
            end_time=tomorrow + timedelta(hours=1),
            responsible="Ana Silva",
            coffee=True,
            people_quantity=6,
            description="Weekly leadership sync",
        ),
        Reservation(
            room_id=rooms[1].id,
            start_time=tomorrow + timedelta(hours=2),
            end_time=tomorrow + timedelta(hours=3),
            responsible="Bruno Costa",
            coffee=False,
            people_quantity=None,
            description="Product roadmap review",
        ),
        Reservation(
            room_id=rooms[2].id,
            start_time=tomorrow + timedelta(hours=1),
            end_time=tomorrow + timedelta(hours=2, minutes=30),
            responsible="Carla Martins",
            coffee=True,
            people_quantity=8,
            description="Client discovery workshop",
        ),
        Reservation(
            room_id=rooms[4].id,
            start_time=tomorrow + timedelta(days=1, hours=1),
            end_time=tomorrow + timedelta(days=1, hours=2),
            responsible="Diego Alves",
            coffee=False,
            people_quantity=None,
            description="Hiring panel",
        ),
        Reservation(
            room_id=rooms[6].id,
            start_time=tomorrow + timedelta(hours=1),
            end_time=tomorrow + timedelta(hours=2),
            responsible="Fernanda Rocha",
            coffee=False,
            people_quantity=None,
            description="Budget alignment",
        ),
    ]

    db.add_all(reservations)
    db.commit()

    logger.info(
        "Initial reservations seed created with %s branches, %s rooms, and %s reservations.",
        len(branches),
        len(rooms),
        len(reservations),
    )
