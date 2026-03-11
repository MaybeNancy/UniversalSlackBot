# src/handlers/ping.py
def register(dispatcher):
    dispatcher.register("app_mention", handle_ping)

async def handle_ping(ctx, payload):
    channel = payload["event"]["channel"]
    await ctx.slack.post_message(channel, "pong")
    ctx.logger.info("Ping responded", channel=channel)
