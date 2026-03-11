# src/utils/rate_limiter.py
import asyncio, time

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate                # tokens added per second
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()
        self.lock = asyncio.Lock()

    async def consume(self, n: int = 1):
        async with self.lock:
            now = time.monotonic()
            # refill
            self.tokens = min(self.capacity,
                              self.tokens + (now - self.last) * self.rate)
            self.last = now
            if self.tokens >= n:
                self.tokens -= n
                return
            # not enough – wait
            needed = (n - self.tokens) / self.rate
            await asyncio.sleep(needed)
            self.tokens = 0
