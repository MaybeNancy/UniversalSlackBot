#context
# src/context.py
from dataclasses import dataclass
from src.services.slack_service import SlackService
from src.services.openai_service import OpenAIService
from src.storage.interface import StorageInterface
from src.utils.logging import Logger
import asyncio

@dataclass
class Context:
    slack: SlackService
    openai: OpenAIService
    storage: StorageInterface
    logger: Logger
    semaphore: asyncio.Semaphore

    # a back‑reference to the FastAPI app (set by the router)
    @property
    def app(self):
        # FastAPI stores the app on the request; we keep a tiny reference
        # via the dispatcher that was attached to the app state.
        # This is a convenience; you can also pass the app directly.
        return self.slack._fastapi_app
