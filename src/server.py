import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .globals import globals_start, globals_end

import routes

"""
Fix or use these later:
from src.dispatcher import Dispatcher
from src.services.slack_service import SlackService
"""

def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #We init the client and many stuff
        #Semaphore thingy?
        #Slack init?
        globals_start()
        yield
        globals_end()
        
    app = FastAPI(title="Universal Slack Bot",lifespan=lifespan)

    #mount routes from src/routes.py
    app.include_router(routes.router)
    
    return app
