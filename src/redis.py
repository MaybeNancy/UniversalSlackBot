##### client
from upstash_redis.asyncio import Redis

_redis: Redis | None = None

def get_redis() -> Redis:
    assert _redis is not None, "Redis client not initialized"
    return _redis

async def startup_redis():
    global _redis
    if _redis is None:
        _redis = Redis.from_env()  # reads UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN

async def shutdown_redis():
    global _redis
    if _redis is not None:
        # Redis is an async context manager; ensure any session cleanup if used
        try:
            await _redis.close()
        except Exception:
            pass
        _redis = None

###### Cache upstash
import json
from app.redis_client import get_redis

async def cache_get(key: str):
    r = get_redis()
    v = await r.get(key)
    return json.loads(v) if v else None

async def cache_set(key: str, value, ttl: int = 300):
    r = get_redis()
    await r.set(key, json.dumps(value))
    if ttl:
        await r.expire(key, ttl)
