#context
# src/context.py
from dataclasses import dataclass
from src.services.slack_service import SlackService
import asyncio

@dataclass
class Context:
    slack: SlackService
    semaphore: asyncio.Semaphore

    # a back‑reference to the FastAPI app (set by the router)
    @property
    def app(self):
        # FastAPI stores the app on the request; we keep a tiny reference
        # via the dispatcher that was attached to the app state.
        # This is a convenience; you can also pass the app directly.
        return self.slack._fastapi_app
