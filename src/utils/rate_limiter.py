import asyncio, time

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        # rate: tokens added per second; capacity: max stored tokens
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()
        self.lock = asyncio.Lock()

    async def consume(self, n: int = 1):
        # Consume n tokens, waiting if necessary until tokens refill
        async with self.lock:
            now = time.monotonic()
            # refill tokens based on elapsed time
            self.tokens = min(self.capacity,
                              self.tokens + (now - self.last) * self.rate)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return
            # Not enough tokens — sleep until enough accumulate
            needed = (n - self.tokens) / self.rate
            await asyncio.sleep(needed)
            self.tokens = 0
