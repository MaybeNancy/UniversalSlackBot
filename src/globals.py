import asyncio
import httpx
#httpx or session
client = None
#semaphore

def globals_start():
  #aquire the slack credentiaks
  #da credentials
  #twitter credentials
  #perchance credentials?
  TIMEOUT = httpx.Timeout(8.0, connect=2.0)
  LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
  
  global client
  client = httpx.AsyncClient(timeout=TIMEOUT, limits=LIMITS)
  #start semaphore

def globals_end():
  client.aclose()
  #end semaphore

def return_client(): return client
