"""Script one-time: bikin semua file template DocKit untuk FastAPI."""
import os

BASE = os.path.join("generator", "templates", "fastapi")

FILES = {
    # ---------- file kosong ----------
    "base/app/__init__.py.j2": "",
    "base/app/api/__init__.py.j2": "",
    "base/app/api/routes/__init__.py.j2": "",
    "base/app/core/__init__.py.j2": "",
    "base/app/models/__init__.py.j2": "",
    "base/app/schemas/__init__.py.j2": "",
    "base/app/services/__init__.py.j2": "",
    "base/tests/__init__.py.j2": "",

    # ---------- base: app ----------
    "base/app/main.py.j2": r'''from contextlib import asynccontextmanager

from fastapi import FastAPI
{% if db_enabled %}
from app.api.routes import items
from app.core.database import engine
from app.models.base import Base
{% endif %}
{% if redis_enabled %}
from app.api.routes import cache
{% endif %}
from app.api.routes import health
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
{% if db_enabled %}
    Base.metadata.create_all(bind=engine)
{% endif %}
    yield


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.include_router(health.router, tags=["Health"])
{% if db_enabled %}
app.include_router(items.router, prefix="/api/v1")
{% endif %}
{% if redis_enabled %}
app.include_router(cache.router, prefix="/api/v1")
{% endif %}
''',

    "base/app/core/config.py.j2": r'''from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "{{ project_name }}"
    ENVIRONMENT: str = "development"
{% if db_enabled %}
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "dockit"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "{{ project_name }}"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
{% endif %}
{% if redis_enabled %}
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
{% endif %}

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
''',

    "base/app/api/routes/health.py.j2": r'''from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}
''',

    # ---------- base: root files ----------
    "base/requirements.txt.j2": r'''fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic-settings==2.5.2
{% if db_enabled %}
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
{% endif %}
{% if redis_enabled %}
redis==5.1.0
{% endif %}
pytest==8.3.3
httpx==0.27.2
''',

    "base/Dockerfile.j2": r'''FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''',

    "base/docker-compose.yml.j2": r'''services:
  app:
    build: .
    container_name: {{ project_name }}_app
    ports:
      - "8000:8000"
    volumes:
      - ./:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
{% if db_enabled or redis_enabled %}
    depends_on:
{% if db_enabled %}
      - db
{% endif %}
{% if redis_enabled %}
      - redis
{% endif %}
{% endif %}

{% if db_enabled %}
  db:
    image: postgres:16-alpine
    container_name: {{ project_name }}_db
    environment:
      POSTGRES_USER: ${DB_USER:-dockit}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
      POSTGRES_DB: ${DB_NAME:-{{ project_name }}}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
{% endif %}

{% if redis_enabled %}
  redis:
    image: redis:7-alpine
    container_name: {{ project_name }}_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
{% endif %}

{% if db_enabled or redis_enabled %}
volumes:
{% if db_enabled %}
  postgres_data:
{% endif %}
{% if redis_enabled %}
  redis_data:
{% endif %}
{% endif %}
''',

    "base/.env.example.j2": r'''APP_NAME={{ project_name }}
ENVIRONMENT=development
{% if db_enabled %}
DB_HOST=db
DB_PORT=5432
DB_USER=dockit
DB_PASSWORD=secret
DB_NAME={{ project_name }}
{% endif %}
{% if redis_enabled %}
REDIS_HOST=redis
REDIS_PORT=6379
{% endif %}
''',

    "base/.gitignore.j2": r'''__pycache__/
*.py[cod]
.venv/
venv/
.env
.pytest_cache/
.ruff_cache/
.DS_Store
''',

    "base/tests/test_health.py.j2": r'''from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
''',

    "base/README.md.j2": r'''# {{ project_name }}

Generated with **DocKit** - Docker Development Kit.

## Stack
- FastAPI
{% if db_enabled %}
- PostgreSQL (SQLAlchemy)
{% endif %}
{% if redis_enabled %}
- Redis
{% endif %}
- Docker & Docker Compose

## Installation

```bash
cp .env.example .env
docker compose up --build
```

## Access
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
{% if db_enabled %}
- PostgreSQL: localhost:5432
{% endif %}
{% if redis_enabled %}
- Redis: localhost:6379
{% endif %}

## Testing

```bash
docker compose exec app pytest
```
''',

    # ---------- addon: postgres ----------
    "addons/postgres/app/core/database.py.j2": r'''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''',

    "addons/postgres/app/models/base.py.j2": r'''from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
''',

    "addons/postgres/app/models/item.py.j2": r'''from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    is_active = Column(Boolean, default=True)
''',

    "addons/postgres/app/schemas/item.py.j2": r'''from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    name: str
    description: str | None = None


class ItemOut(ItemCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
''',

    "addons/postgres/app/api/routes/items.py.j2": r'''from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemOut

router = APIRouter(tags=["Items"])


@router.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
''',

    # ---------- addon: redis ----------
    "addons/redis/app/core/cache.py.j2": r'''import redis

from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
''',

    "addons/redis/app/api/routes/cache.py.j2": r'''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.cache import redis_client

router = APIRouter(tags=["Cache"])


class CacheSet(BaseModel):
    key: str
    value: str
    ttl: int | None = 60


@router.post("/cache")
def cache_set(payload: CacheSet):
    redis_client.set(payload.key, payload.value, ex=payload.ttl)
    return {"status": "stored", "key": payload.key}


@router.get("/cache/{key}")
def cache_get(key: str):
    value = redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found or expired")
    return {"key": key, "value": value}
''',
}


def main():
    for rel, content in FILES.items():
        path = os.path.join(BASE, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print("created:", path)
    print(f"\nDone! {len(FILES)} files created.")


if __name__ == "__main__":
    main()