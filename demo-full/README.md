# demo_full

Generated with **DocKit** - Docker Development Kit.

## Stack
- FastAPI
- PostgreSQL (SQLAlchemy)
- Redis
- Docker & Docker Compose

## Installation

```bash
cp .env.example .env
docker compose up --build
```

## Access
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Testing

```bash
docker compose exec app pytest
```
