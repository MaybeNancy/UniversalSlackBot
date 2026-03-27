import asyncio
import httpx
import os

from upstash_redis.asyncio import Redis
#httpx or session
client = None
BOT_TOKEN = None
SLACK_SECRET = None

#REDIS
REDIS = None

async def globals_start():
  #aquire the slack credentiaks
  #da credentials
  #twitter credentials
  #perchance credentials?
  TIMEOUT = httpx.Timeout(8.0, connect=2.0)
  LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
  
  global client
  client = httpx.AsyncClient(timeout=TIMEOUT, limits=LIMITS)

  global REDIS
  REDIS = Redis.from_env()

  global BOT_TOKEN
  BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
  global SLACK_SECRET
  SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")
  #start semaphore

async def globals_end():
  await client.aclose()
  await REDIS.close()
  #end semaphore

def return_client(): return client
def return_redis(): return REDIS

def return_b_token(): return BOT_TOKEN
def return_s_secret(): return SLACK_SECRET
