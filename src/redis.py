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

####### rate limiter
from app.redis_client import get_redis

async def rate_allowed(identifier: str, limit: int = 10, window: int = 60) -> bool:
    r = get_redis()
    key = f"rate:{identifier}"
    cur = await r.incr(key)
    if cur == 1:
        await r.expire(key, window)
    return cur <= limit

###### dedupe stash
from app.redis_client import get_redis

async def try_dedupe(event_id: str, ttl: int = 60) -> bool:
    r = get_redis()
    key = f"dedup:{event_id}"
    ok = await r.set(key, "1", nx=True)
    if ok and ttl:
        await r.expire(key, ttl)
    return bool(ok)

###### locks upstash
import uuid
from app.redis_client import get_redis

_RELEASE_SCRIPT = """
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])
else
  return 0
end
"""

async def acquire_lock(name: str, ttl: int = 10) -> str | None:
    r = get_redis()
    token = str(uuid.uuid4())
    ok = await r.set(name, token, nx=True)
    if ok and ttl:
        await r.expire(name, ttl)
    return token if ok else None

async def release_lock(name: str, token: str) -> bool:
    r = get_redis()
    res = await r.eval(_RELEASE_SCRIPT, 1, name, token)
    return res == 1
