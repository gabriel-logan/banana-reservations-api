import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.common.exceptions import AppException
from app.common.responses import ErrorResponse
from app.core.config import settings
from app.infrastructure.database.migrate import run_migrations
from app.infrastructure.database.session import SessionLocal
from app.modules.branches.entity import Branch
from app.modules.branches.routes import router as branches_router
from app.modules.rooms.entity import Room
from app.modules.rooms.routes import router as rooms_router
from app.modules.reservations.routes import router as reservations_router

app = FastAPI(title="Banana Reservations API")
allowed_domains = [
    domain.strip()
    for domain in settings.allowed_domains.split(",")
    if domain.strip()
]

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
    run_migrations()
    seed_initial_data()


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


def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Branch.id).count() > 0:
            return

        matriz = Branch(name="Matriz")
        paulista = Branch(name="Paulista")
        db.add_all([matriz, paulista])
        db.flush()

        db.add_all(
            [
                Room(name="Sala Sol", branch_id=matriz.id),
                Room(name="Sala Lua", branch_id=matriz.id),
                Room(name="Sala Oceano", branch_id=paulista.id),
            ]
        )
        db.commit()
    finally:
        db.close()
