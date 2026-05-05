import asyncio
from ..globals import return_client

link = "https://perchance.org/api/generate"
TEMPLATE = "nancy-ai-module"

async def call_site():
  client = return_client()

  headers={
    "User-Agent": "MyBot/1.0",
    "Referer": "https://perchance.org/"
  }
  
  params = {"template": TEMPLATE}
  
  resp = await client.get(link,headers=headers, params=params)
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
