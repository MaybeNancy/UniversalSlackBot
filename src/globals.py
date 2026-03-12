import asyncio
#httpx or session
client = None
#semaphore

def start_globals():
  TIMEOUT = httpx.Timeout(8.0, connect=2.0)
  LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
  client = httpx.AsyncClient(timeout=TIMEOUT, limit=LIMITS)

def end_globals()
  client.aclose()
