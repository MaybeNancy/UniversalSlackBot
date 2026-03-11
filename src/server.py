import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.routes import router
from src.dispatcher import Dispatcher
from src.services.slack_service import SlackService

#Delete this later
from src.utils.logging import get_logger

client = None

def create_app():
    logger = get_logger() #<- To be deleted
    
    app = FastAPI(title="Universal Slack Bot")

    app.include_router(router)  # mount routes from src/routes.py

    client = httpx.AsyncClient(timeout=10)
    
    @app.on_event("startup")
    async def startup():
        # Create singletons at startup to avoid import-time side effects.
        app.state.slack = SlackService()                 # Slack API helper (reads env vars)
        app.state.slack._fastapi_app = app               # back-reference used by Context.app
        # Attach a logger so handlers can call ctx.slack.logger or ctx.logger
        app.state.slack.logger = get_logger("duckbot")
        app.state.dispatcher = Dispatcher()              # loads handlers under src.handlers
        # global concurrency semaphore (default 10); stored on app.state for handlers to use
        app.state.semaphore = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENCY", "10")))

    @app.on_event("shutdown")
    async def shutdown():
        # Close httpx AsyncClient to free resources on shutdown
        try:
            await app.state.slack.client.aclose()
        except Exception:
            printf("oh no")
    return app
