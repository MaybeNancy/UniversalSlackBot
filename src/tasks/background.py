import asyncio

async def run_in_background(ctx, payload: dict):
    dispatcher = ctx.app.state.dispatcher
    await dispatcher.dispatch(ctx, payload)
