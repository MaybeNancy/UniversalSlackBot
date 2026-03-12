import asyncio
#httpx or session
client = None
#semaphore

def globals_start():
  TIMEOUT = httpx.Timeout(8.0, connect=2.0)
  LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
  client = httpx.AsyncClient(timeout=TIMEOUT, limit=LIMITS)

def globals_end():
  client.aclose()

def return_client(): return client
