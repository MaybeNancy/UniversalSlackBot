import asyncio
from ..globals import return_client

link = "https://perchance.org/nancy-ai-module"

async def call_site():
  client = return_client()

  headers={
    "User-Agent": "MyBot/1.0",
    "Referer": "https://perchance.org/"
  }
  
  data={"data":"hi"}

  
  resp = await client.get(link)
  print(resp.status_code)
  print(resp.headers)

  
  return "hu"
