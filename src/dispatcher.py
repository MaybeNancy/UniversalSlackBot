import json, asyncio

from .handlers.ping import reply

async def message(data):
    return reply(data)

event_routes = {
    "message":message,
    "mention":message
}

async def event_dispatch(data):
    type = data.get("type")
    if type == "event_callback":
        event_d = data.get("event")
        event = event_d["type"]
        
        if event in event_routes:
            handler = event_routes[event]
            return await handler(event_d)
