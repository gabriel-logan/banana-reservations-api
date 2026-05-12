# banana-reservations-api

Reservations microservice — FastAPI.

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret key for validating JWT tokens |

## Recommended: Run with Docker

```bash
docker compose up --build

# or

docker-compose up --build
```

This starts:

- **reservations-api** — FastAPI on port 8000
- **postgres-reservations** — PostgreSQL database

## Manual setup

*Not recommended.*

Requires:

- PostgreSQL installed locally
- Reservations database created manually
- Environment variables configured manually

```bash
uvicorn app.main:app --reload --app-dir src
```
