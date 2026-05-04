import asyncio
from ..globals import return_client

link = "https://perchance.org/nancy-ai-module"

async def call_site():
  client = return_client()
  
  data="Hi"

  """
  resp = await client.post(
            link,
            json=data,
  )
  """
  resp = await client.get(link)
  print(resp.status_code)
  print(await resp.text())

  
  return resp
