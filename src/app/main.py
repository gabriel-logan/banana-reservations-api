import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI

from app.modules.branches.routes import router as branches_router
from app.modules.rooms.routes import router as rooms_router
from app.modules.reservations.routes import router as reservations_router

app = FastAPI(title="Banana Reservations API")

app.include_router(branches_router)
app.include_router(rooms_router)
app.include_router(reservations_router)


@app.get("/")
def health():
    return {"status": "ok"}
