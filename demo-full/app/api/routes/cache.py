from fastapi import APIRouter, HTTPException
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
