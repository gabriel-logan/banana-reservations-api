# banana-reservations-api

Reservations microservice — FastAPI.

## Routes

- **GET /health** — Health check
- **GET /branches** — List branches
- **GET /branches/{branch_id}** — Get one branch
- **POST /branches** — Create a branch. Body: `{ name }`
- **DELETE /branches/{branch_id}** — Delete a branch
- **GET /rooms** — List rooms. Query: `{ branch_id? }`
- **GET /rooms/{room_id}** — Get one room
- **POST /rooms** — Create a room. Body: `{ name, branch_id }`
- **DELETE /rooms/{room_id}** — Delete a room
- **GET /reservations** — List reservations. Query: `{ room_id? }`
- **GET /reservations/{reservation_id}** — Get one reservation
- **POST /reservations** — Create a reservation. Body: `{ branch_id, room_id, start_time, end_time, responsible, coffee, people_quantity?, description? }`
- **PUT /reservations/{reservation_id}** — Update a reservation. Body: `{ branch_id, room_id, start_time, end_time, responsible, coffee, people_quantity?, description? }`
- **DELETE /reservations/{reservation_id}** — Delete a reservation

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
