import asyncio
import httpx
import os

from upstash_redis.asyncio import Redis
#httpx or session
client = None

#Slack
BOT_TOKEN = None
SLACK_SECRET = None

#DA
DA_ID = None
DA_SECRET = None

#AI
HF_TOKEN = None #HuggingFace
OR_TOKEN = None #OpenRouter

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

  #start REDIS
  global REDIS
  REDIS = Redis.from_env()

  global BOT_TOKEN
  BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
  global SLACK_SECRET
  SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")

  global DA_ID
  DA_TOKEN = os.getenv("DA_API_ID")
  global DA_SECRET
  DA_TOKEN = os.getenv("DA_API_SECRET")
  
  global HF_TOKEN
  HF_TOKEN = os.getenv("SLACKNEURON")
  global OR_TOKEN
  OR_TOKEN = os.getenv("SLACKNEURON2")

async def globals_end():
  await client.aclose()
  await REDIS.close()

def return_client(): return client
def return_redis(): return REDIS

def return_b_token(): return BOT_TOKEN
def return_s_secret(): return SLACK_SECRET

def return_da_id(): return DA_ID
def return_da_secret(): return DA_SECRET

def r_hug_token(): return HF_TOKEN
def r_or_token(): return OR_TOKEN
