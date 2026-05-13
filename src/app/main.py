import logging
import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.common.exceptions import AppException
from app.common.responses import ErrorResponse
from app.core.config import settings
from app.infrastructure.database.migrate import run_migrations
from app.infrastructure.database.seeder import seed_initial_data
from app.infrastructure.database.session import SessionLocal
from app.modules.branches.routes import router as branches_router
from app.modules.rooms.routes import router as rooms_router
from app.modules.reservations.routes import router as reservations_router

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.DEBUG),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(title="Banana Reservations API")
logger = logging.getLogger(__name__)
allowed_domains = []


def expand_allowed_domains(raw_allowed_domains: str) -> list[str]:
    expanded_domains: list[str] = []

    for domain in raw_allowed_domains.split(","):
        normalized_domain = domain.strip()

        if not normalized_domain:
            continue

        if normalized_domain not in expanded_domains:
            expanded_domains.append(normalized_domain)

        try:
            from urllib.parse import urlparse

            parsed_domain = urlparse(normalized_domain)
        except ValueError:
            continue

        if parsed_domain.hostname not in {"localhost", "127.0.0.1", "::1"}:
            continue

        port = f":{parsed_domain.port}" if parsed_domain.port else ""

        for alias in (
            f"{parsed_domain.scheme}://localhost{port}",
            f"{parsed_domain.scheme}://127.0.0.1{port}",
            f"{parsed_domain.scheme}://[::1]{port}",
        ):
            if alias not in expanded_domains:
                expanded_domains.append(alias)

    return expanded_domains


allowed_domains = expand_allowed_domains(settings.allowed_domains)

if settings.allowed_domains.strip() == "*" or not allowed_domains:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_domains,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def startup():
    try:
        logger.info("Starting Banana Reservations API.")
        logger.debug("Running database migrations.")
        run_migrations()
        logger.debug("Database migrations finished.")

        with SessionLocal() as db:
            seed_initial_data(db)

        logger.info("Banana Reservations API startup completed.")
    except Exception as exc:
        print("Reservations API startup failed:", repr(exc), file=sys.stderr, flush=True)
        traceback.print_exc()
        logger.exception("Reservations API startup failed.")
        raise


@app.exception_handler(AppException)
def handle_app_exception(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.message,
            status_code=exc.status_code,
        ).model_dump(by_alias=True),
    )


@app.exception_handler(RequestValidationError)
def handle_validation_exception(request: Request, exc: RequestValidationError):
    errors: dict[str, list[str]] = {}

    for error in exc.errors():
        location = str(error["loc"][-1]) if len(error["loc"]) > 1 else "body"
        errors.setdefault(location, []).append(error["msg"])

    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed.",
            "statusCode": 422,
            "errors": errors,
            "traceId": request.headers.get("x-request-id"),
        },
    )

app.include_router(branches_router)
app.include_router(rooms_router)
app.include_router(reservations_router)


@app.get("/health")
def health():
    return {"status": "ok"}
