# banana-reservations-api

Reservations microservice — FastAPI.

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret key for validating JWT tokens |

## Run locally

```bash
uvicorn app.main:app --reload
```

## Run with Docker

```bash
docker compose up --build
```
