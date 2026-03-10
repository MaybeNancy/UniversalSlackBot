#pong
# src/handlers/ping.py
def register(dispatcher):
    dispatcher.register("app_mention", handle_ping)

async def handle_ping(payload, slack, store):
    channel = payload["event"]["channel"]
    await slack.post_message(channel, "pong")
