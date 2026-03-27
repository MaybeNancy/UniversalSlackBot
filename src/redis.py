
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

##### sessions uptash
from app.redis_client import get_redis

async def set_conv(user_id: str, mapping: dict, ttl: int = 300):
    r = get_redis()
    key = f"conv:{user_id}"
    # hset accepts str/int/float/bool values in Upstash; serialize complex values
    await r.hset(key, mapping={k: (v if isinstance(v, (str,int,float,bool)) else str(v)) for k,v in mapping.items()})
    if ttl:
        await r.expire(key, ttl)

async def get_conv(user_id: str) -> dict:
    r = get_redis()
    key = f"conv:{user_id}"
    return await r.hgetall(key)

### flags
from app.redis_client import get_redis

async def set_flag(name: str, value: str):
    r = get_redis()
    await r.set(f"flag:{name}", value)

async def get_flag(name: str) -> str | None:
    r = get_redis()
    return await r.get(f"flag:{name}")

##analitics
from app.redis_client import get_redis

async def incr_counter(name: str, by: int = 1):
    r = get_redis()
    await r.incrby(f"metrics:{name}", by)

async def add_score(leaderboard: str, member: str, score: float):
    r = get_redis()
    await r.zincrby(f"leaderboard:{leaderboard}", score, member)

async def top_scores(leaderboard: str, top_n: int = 10):
    r = get_redis()
    return await r.zrevrange(f"leaderboard:{leaderboard}", 0, top_n - 1, withscores=True)

###heartbeat upstash
from app.redis_client import get_redis
import os

INSTANCE_ID = os.getenv("INSTANCE_ID", "instance:local")

async def heartbeat(ttl: int = 30):
    r = get_redis()
    await r.set(f"instance:{INSTANCE_ID}:alive", "1")
    if ttl:
        await r.expire(f"instance:{INSTANCE_ID}:alive", ttl)

async def active_instances():
    r = get_redis()
    return await r.keys("instance:*:alive")

#####queue upstash
import json
from app.redis_client import get_redis

STREAM_KEY = "stream:tasks"
GROUP = "workers"
CONSUMER_PREFIX = "c-"

async def ensure_group():
    r = get_redis()
    try:
        await r.xgroup_create(STREAM_KEY, GROUP, "$", mkstream=True)
    except Exception:
        # ignore if exists
        pass

async def publish_task(payload: dict):
    r = get_redis()
    await r.xadd(STREAM_KEY, {"data": json.dumps(payload)})

async def read_group(consumer_id: str = "1", count: int = 10, block: int = 5000):
    r = get_redis()
    consumer = CONSUMER_PREFIX + consumer_id
    entries = await r.xreadgroup(GROUP, consumer, {STREAM_KEY: ">"}, count=count, block=block)
    return entries  # format: [(stream, [(id, {b'data': b'...'})...])]

async def ack(message_id: str):
    r = get_redis()
    await r.xack(STREAM_KEY, GROUP, message_id)

###stream worker
import asyncio
import json
import os
from app.redis_client import startup_redis, shutdown_redis, get_redis
from app.queue_upstash import ensure_group, read_group, ack

CONSUMER_ID = os.getenv("INSTANCE_ID", "worker1")

async def handle_message(message_id: str, payload_raw: bytes):
    payload = json.loads(payload_raw)
    # implement processing logic here (call your event_dispatch, httpx calls, etc.)
    # example: await event_dispatch(payload)
    await asyncio.sleep(0)  # placeholder

async def worker_loop():
    await startup_redis()
    await ensure_group()
    try:
        while True:
            entries = await read_group(CONSUMER_ID, count=10, block=5000)
            if not entries:
                continue
            # entries: [(stream, [(id, {'data': '...'}), ...])]
            for _, msgs in entries:
                for message_id, fields in msgs:
                    data = fields.get("data")
                    try:
                        await handle_message(message_id, data)
                        await ack(message_id)
                    except Exception:
                        # optionally log and don't ack to allow retries
                        pass
    finally:
        await shutdown_redis()

if __name__ == "__main__":
    asyncio.run(worker_loop())

#NOTES: 
"""
Upstash REST clients are connectionless; Redis.from_env() reads UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN.
Streams are recommended for reliability (XADD / XREADGROUP / XACK) rather than Pub/Sub over REST.
Batch operations and minimizing commands reduces Upstash request counts and cost.
"""
