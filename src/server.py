import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

"""
Fix or use these later:
from src.routes import router
from src.dispatcher import Dispatcher
from src.services.slack_service import SlackService
"""

client = None

def create_app():
    #We init the client
    TIMEOUT = httpx.Timeout(8.0, connect=2.0)
    LIMITS = httpx.Limits(max_connections=10,max_keepalive_connections=5)
    client = httpx.AsyncClient(timeout=TIMEOUT, limit=LIMITS)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #InitDispatcher
        #Semaphoren thingy
        #Slack init?
        yield
        client.aclose()
        
    app = FastAPI(title="Universal Slack Bot",lifespan=lifespan)

    #mount routes from src/routes.py
    app.include_router(router)
    
    return app
