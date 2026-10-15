import asyncio
import httpx
import os

from huggingface_hub import InferenceClient
from openai import OpenAI

from upstash_redis.asyncio import Redis
#httpx or session
client = None

#Slack
BOT_TOKEN = None
SLACK_SECRET = None
NANCY = None

#DA
DA_ID = None
DA_SECRET = None

#AI
HF_client = None #HuggingFace
OR_client = None #OpenRouter
model = "deepseek-ai/DeepSeek-V4-Pro:novita"

#REDIS
REDIS = None

async def globals_start():
    #aquire the slack credentiaks
    #da credentials
    #twitter credentials
    
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

    global NANCY
    NANCY = os.getenv("NANCY")

    global DA_ID
    DA_TOKEN = os.getenv("DA_API_ID")
    global DA_SECRET
    DA_TOKEN = os.getenv("DA_API_SECRET")

    global HF_client
    HF_client = InferenceClient(
        token=os.getenv("SLACKNEURON"),
        timeout=30,
        model=model
    )

    global OR_client
    OR_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("SLACKNEURON2")
    )

async def globals_end():
    await client.aclose()
    await REDIS.close()

def return_client(): return client
def return_redis(): return REDIS

def return_b_token(): return BOT_TOKEN
def return_s_secret(): return SLACK_SECRET
def r_nancy():return NANCY

def return_da_id(): return DA_ID
def return_da_secret(): return DA_SECRET

def r_hug_client(): return HF_client
def r_or_client(): return OR_client
