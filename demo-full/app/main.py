from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes import items
from app.core.database import engine
from app.models.base import Base
from app.api.routes import cache
from app.api.routes import health
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.include_router(health.router, tags=["Health"])
app.include_router(items.router, prefix="/api/v1")
app.include_router(cache.router, prefix="/api/v1")
