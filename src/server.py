# src/server.py
import asyncio
from fastapi import FastAPI
from src.routes import router
from src.dispatcher import Dispatcher
from src.utils.logging import get_logger

def create_app() -> FastAPI:
    logger = get_logger()
    app = FastAPI(title="Universal Slack Bot")

    # health endpoint lives in the router
    app.include_router(router)

    # one global dispatcher and a semaphore for all background calls
    app.state.dispatcher = Dispatcher()
    app.state.semaphore = asyncio.Semaphore(int(
        # allow overriding via env, default 10 concurrent external calls
        __import__("os").getenv("MAX_CONCURRENCY", "10")
    ))

    # src/server.py (add at the end of create_app)
    # expose the FastAPI app to the dispatcher via a back‑reference
    app.state.dispatcher.app = app   # type: ignore


    logger.info("FastAPI app created")
    return app
