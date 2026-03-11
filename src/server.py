import asyncio
import os
from fastapi import FastAPI
from src.routes import router
from src.dispatcher import Dispatcher
from src.services.slack_service import SlackService
from src.utils.logging import get_logger

def create_app() -> FastAPI:
    logger = get_logger()
    app = FastAPI(title="Duck.ai Slack Bot")

    app.include_router(router)

    @app.on_event("startup")
    async def startup():
        app.state.slack = SlackService()
        app.state.slack._fastapi_app = app
        app.state.dispatcher = Dispatcher()
        app.state.semaphore = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENCY", "10")))
        logger.info("App startup complete")

    @app.on_event("shutdown")
    async def shutdown():
        try:
            await app.state.slack.client.aclose()
        except Exception:
            logger.exception("Error closing SlackService client")

    logger.info("FastAPI app created")
    return app
