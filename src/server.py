import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

import globals

"""
Fix or use these later:
from src.routes import router
from src.dispatcher import Dispatcher
from src.services.slack_service import SlackService
"""

client = None

def create_app():
    #We init the client

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #InitDispatcher
        #Semaphoren thingy
        #Slack init?
        globals_start()
        yield
        globals_end()
        #client.aclose()
        
    app = FastAPI(title="Universal Slack Bot",lifespan=lifespan)

    #mount routes from src/routes.py
    app.include_router(router)
    
    return app
