#httpx or session
client = None
#semaphore

def start_globals():
  client = httpx.AssyncC()

def end_globals()
