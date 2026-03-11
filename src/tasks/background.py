# src/tasks/background.py
import asyncio

async def run_in_background(ctx, payload: dict):
    """Called by FastAPI's BackgroundTasks after the ACK."""
    dispatcher = ctx.app.state.dispatcher   # dispatcher stored on the FastAPI app
    await dispatcher.dispatch(ctx, payload)
