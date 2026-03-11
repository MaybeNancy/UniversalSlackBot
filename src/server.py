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

    #We knit the client
    TIMEOUT = httpx.Timeout(8.0, connect=2.0)
    LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
    client = httpx.AsyncClient(timeout=TIMEOUT, limit=LIMITS)

    #This will change btw, on_event is deprecated
    @app.on_event("startup")
    async def startup():
        app.state.dispatcher = Dispatcher()
        # global concurrency semaphore (default 10); stored on app.state for handlers to use
        app.state.semaphore = asyncio.Semaphore(10)

    @app.on_event("shutdown")
    async def shutdown():
        # Close httpx AsyncClient to free resources on shutdown
        try:
            await app.state.slack.client.aclose()
        except Exception:
            printf("oh no")
    return app
