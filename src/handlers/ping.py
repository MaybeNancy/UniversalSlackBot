def register(dispatcher):
    # Called by Dispatcher._load_handlers to register handlers
    dispatcher.register("app_mention", handle_ping)

async def handle_ping(ctx, payload):
    # Example handler: respond "pong" when bot is mentioned
    channel = payload["event"]["channel"]
    await ctx.slack.post_message(channel, "pong")
    # Use ctx.logger if present; fallback to ctx.slack.logger
    if hasattr(ctx, "logger"):
        ctx.logger.info("Ping responded", channel=channel)
    elif hasattr(ctx.slack, "logger"):
        ctx.slack.logger.info("Ping responded", channel=channel)
