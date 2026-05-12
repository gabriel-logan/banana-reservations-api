from fastapi import FastAPI

app = FastAPI(title="Banana Reservations API")

@app.get("/")
def health():
    return {"status": "ok"}

