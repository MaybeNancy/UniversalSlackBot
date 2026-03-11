from dataclasses import dataclass
from src.services.slack_service import SlackService
import asyncio

#what is this for exactly?

@dataclass
class Context:
    slack: SlackService
    semaphore: asyncio.Semaphore

    # Convenience property to access the FastAPI app via slack._fastapi_app
    @property
    def app(self):
        return self.slack._fastapi_app
