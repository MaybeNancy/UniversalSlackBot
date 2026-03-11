#I don't know what this thimg even do
#but sounds useful, might check later.
import asyncio

async def run_in_background(ctx, payload: dict):
    # FastAPI BackgroundTasks calls this after ACK. It delegates to the app's Dispatcher.
    dispatcher = ctx.app.state.dispatcher   # Dispatcher attached to FastAPI app at startup
    await dispatcher.dispatch(ctx, payload) # await handler(s) for the event
