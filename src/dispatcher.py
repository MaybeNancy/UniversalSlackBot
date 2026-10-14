import json, asyncio

from .handlers.mention import reply
from .handlers.chatted import get_message

from .chatbot.orchestrator import think

event_routes = {
    "app_mention": reply,
    "message": get_message
}

async def event_dispatch(data):
    type = data.get("type")
    if type == "event_callback":
        event_d = data.get("event")
        event = event_d["type"]

        if event in event_routes:
            handler = event_routes[event]
            await think()
            return await handler(event_d)
