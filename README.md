# banana-reservations-api

Reservations microservice for Banana Meeting Rooms.

## Responsibility

- Manage branches
- Manage rooms
- Manage reservations
- Validate reservation conflicts
- Validate JWT tokens issued by `banana-auth-api`

## Tech Choices

- **FastAPI** because the challenge allows Python frameworks and FastAPI gives a very good balance between speed of implementation, readability and built-in validation. I chose it over Flask because Flask would require more manual structuring for request validation and API contracts, and over Django because Django would be heavier than necessary for a focused microservice.
- **SQLAlchemy** because the project needs a relational ORM with explicit models and predictable queries. I chose it over smaller ORMs because SQLAlchemy is more established, flexible and easier to scale in complexity if business rules around reservations grow. It also keeps the repository layer explicit instead of hiding too much behind framework conventions.
- **Alembic** because schema evolution needs to be versioned and repeatable. I chose it over relying only on automatic table creation because migrations document database changes clearly and make the service more reliable to run in different environments.
- **PostgreSQL** because reservation data has relational constraints and conflict rules that fit well in a relational database. I chose it over SQLite because this project benefits from a database engine closer to real-world concurrency and deployment scenarios, while still being lightweight enough for local Docker usage.
- **Shared JWT secret validation** because this microservice only needs to verify tokens issued by the auth service, not manage user credentials directly. I chose this approach over calling the auth API on every request because local JWT validation keeps the reservations service independent, faster and better aligned with the proposed microservice architecture.

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

## How This API Works

This service receives all business requests related to branches, rooms and reservations. Every business route is protected, so the frontend must send a JWT in the `Authorization` header. Before processing the request, the API validates that token locally using the shared `JWT_SECRET` and extracts the authenticated user identity from the token payload.

Once the user is identified, the API executes the requested operation in its own PostgreSQL database. Listing routes return branches, rooms or reservations, and reservation queries are scoped by authenticated user where applicable. Create and update operations also validate business rules such as branch existence, room existence, room-to-branch consistency and time range validity.

The most important rule in this service is conflict detection. Before creating or updating a reservation, the API checks whether another reservation already exists for the same room in an overlapping time interval. If so, the request is rejected with a conflict response. This keeps the final scheduling guarantee in the backend even if the frontend already filtered available options earlier.

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
