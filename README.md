# banana-reservations-api

Reservations microservice — FastAPI.

## Routes

- **GET /health** — Health check
- **GET /branches** — List branches
- **GET /branches/{branch_id}** — Get one branch. Path: `{ branch_id }`
- **POST /branches** — Create a branch. Body: `{ name }`
- **DELETE /branches/{branch_id}** — Delete a branch. Path: `{ branch_id }`
- **GET /rooms** — List rooms. Query: `{ branchId? }`
- **GET /rooms/{room_id}** — Get one room. Path: `{ room_id }`
- **POST /rooms** — Create a room. Body: `{ name, branchId }`
- **DELETE /rooms/{room_id}** — Delete a room. Path: `{ room_id }`
- **GET /reservations** — List reservations. Query: `{ roomId? }`
- **GET /reservations/{reservation_id}** — Get one reservation. Path: `{ reservation_id }`
- **POST /reservations** — Create a reservation. Body: `{ branchId, roomId, startTime, endTime, responsible, coffee, peopleQuantity, description }`
- **PUT /reservations/{reservation_id}** — Update a reservation. Path: `{ reservation_id }`. Body: `{ branchId, roomId, startTime, endTime, responsible, coffee, peopleQuantity, description }`
- **DELETE /reservations/{reservation_id}** — Delete a reservation. Path: `{ reservation_id }`

All business routes require `Authorization: Bearer <token>`.

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET` | Secret key for validating JWT tokens |

## Database

The service uses SQLAlchemy with PostgreSQL.

Schema changes are managed with Alembic migrations and applied automatically on startup.

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
- Environment variables configured manually

```bash
uvicorn app.main:app --reload --app-dir src
```
