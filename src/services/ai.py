"""
AI billing considerations:

@Monthly credits, like railway

*Prefer CPU models for development, 
batch small requests, and set conservative
parameters (max_tokens, shorter prompts).

*Use small models for prototyping and only
switch to large/GPU models when necessary.

*Monitor usage in the billing/usage dashboard
and set org spending limits if available.

Hub APIs -> 1k requests
Resolvers -> 5k requests
Pages -> 200 requests

Rate limits are applied over 5-minute intervals. 
"""
import asyncio
from ..globals import return_client, r_hug_client

from huggingface_hub import InferenceClient

link = "https://perchance.org/api/generate"
TEMPLATE = "test-n"

async def call_site():
  client = return_client()

  headers={
    "User-Agent": "MyBot/1.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Referer": "https://perchance.org/"
  }
  
  params = {"template": TEMPLATE}
  
  resp = await client.post(link,headers=headers, json={"template": TEMPLATE})
  print(resp.status_code)
  print(resp.headers)
  print(await resp.aread())       # raw body bytes
  try:
            print(resp.json())         # parsed JSON if available
  except Exception:
            pass
  
  return "hu"

"""
import asyncio
import httpx

LINK = "https://perchance.org/api/generate"
TEMPLATE = "nancy-ai-module"  # template name or id

async def call_site():
    async with httpx.AsyncClient(timeout=10.0) as client:
        headers = {
            "User-Agent": "MyBot/1.0",
            "Referer": "https://perchance.org/"
        }
        params = {"template": TEMPLATE}
        resp = await client.get(LINK, headers=headers, params=params)
        print(resp.status_code)
        print(resp.headers)
        print(await resp.aread())       # raw body bytes
        try:
            print(resp.json())         # parsed JSON if available
        except Exception:
            pass
    return "done"

asyncio.run(call_site())
"""
