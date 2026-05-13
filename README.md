# banana-reservations-api

Reservations microservice for Banana Meeting Rooms.

## Responsibility

- Manage branches
- Manage rooms
- Manage reservations
- Validate reservation conflicts
- Validate JWT tokens issued by `banana-auth-api`

## Tech Choices

- **FastAPI** for a lightweight REST API
- **SQLAlchemy** for relational persistence
- **Alembic** for migrations
- **PostgreSQL** as the service database
- **Shared JWT secret** to validate tokens from the auth service

## Requirements

- Docker
- Docker Compose

## Environment Variables

Copy `.env.example` to `.env` and adjust only if needed.

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string used by the API container |
| `JWT_SECRET` | Secret used to validate JWT tokens. It must be exactly the same value used by `banana-auth-api` |
| `ALLOWED_DOMAINS` | Allowed frontend origins separated by comma, or `*` in development |
| `LOG_LEVEL` | Logger level for the API, for example `DEBUG` or `INFO` |

You can keep the shared example value from `.env.example` for quick local testing.

Optional (recommended): generate a stronger shared secret with:

```bash
openssl rand -base64 32
```

## Run

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Database, Migrations and Seeds

- Migrations are applied automatically on startup
- Initial branches, rooms and reservations are seeded automatically on an empty database
- Seed data includes happy-path availability and reservation conflict scenarios

If you want to recreate the database, migrations and seeds from scratch:

```bash
docker compose down -v
docker compose up --build
```

## Routes

- `GET /health`

- `GET /branches`
  Query: `{ start_time?, end_time?, ignore_reservation_id? }`

- `GET /branches/{branch_id}`
  Path: `{ branch_id }`

- `POST /branches`
  Body: `{ name }`

- `DELETE /branches/{branch_id}`
  Path: `{ branch_id }`

- `GET /rooms`
  Query: `{ branch_id?, start_time?, end_time?, ignore_reservation_id? }`

- `GET /rooms/{room_id}`
  Path: `{ room_id }`

- `POST /rooms`
  Body: `{ name, branch_id }`

- `DELETE /rooms/{room_id}`
  Path: `{ room_id }`

- `GET /reservations`
  Query: `{ room_id? }`

- `GET /reservations/{reservation_id}`
  Path: `{ reservation_id }`

- `POST /reservations`
  Body: `{ branch_id, room_id, start_time, end_time, responsible, coffee, people_quantity?, description? }`

- `PUT /reservations/{reservation_id}`
  Path: `{ reservation_id }`
  Body: `{ branch_id, room_id, start_time, end_time, responsible, coffee, people_quantity?, description? }`

- `DELETE /reservations/{reservation_id}`
  Path: `{ reservation_id }`

- `POST /reservations/bulk-delete`
  Body: `{ reservation_ids }`

All business routes require `Authorization: Bearer <token>`.
