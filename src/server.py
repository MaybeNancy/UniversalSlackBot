import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .globals import globals_start, globals_end

from .routes import router

def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        #We init the client and many stuff
        await globals_start()
        yield
        await globals_end()
        
    app = FastAPI(title="Universal Slack Bot",lifespan=lifespan)

    #mount routes from src/routes.py
    app.include_router(router)
    
    return app
