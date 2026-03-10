#src/server.py
from fastapi import FastAPI
from src.routes import router
from src.dispatcher import Dispatcher

def create_app() -> FastAPI:
    app = FastAPI()
    #registers /slack/events and /health
    app.include_router(router)          
    #One global dispatcher
    app.state.dispatcher = Dispatcher()
    return app
