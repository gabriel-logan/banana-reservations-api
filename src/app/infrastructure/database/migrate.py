from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.config import settings


def run_migrations() -> None:
    alembic_ini = _find_alembic_ini()
    config = Config(str(alembic_ini))
    config.set_main_option("script_location", str(_find_alembic_script_location()))
    config.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(config, "head")


def _find_alembic_ini() -> Path:
    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        candidate = parent / "alembic.ini"
        if candidate.exists():
            return candidate

    raise FileNotFoundError("alembic.ini not found.")


def _find_alembic_script_location() -> Path:
    current_file = Path(__file__).resolve()

    for parent in current_file.parents:
        candidate = parent / "alembic"
        if candidate.exists():
            return candidate

    raise FileNotFoundError("Alembic script location not found.")
