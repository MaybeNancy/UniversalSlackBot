import json, asyncio

from .handlers.mention import reply
from .handlers.chatted import check_mess

from .chatbot.orchestrator import think

#element 0 for the method
#element 1 for the context
event_routes = {
    "app_mention": [reply, "mentioned you"],
    "message": [check_mess, "sent something"]
}

async def event_dispatch(data):
    type = data.get("type")
    if type == "event_callback":
        event_d = data.get("event")
        event = event_d["type"]

        if event in event_routes:
            handler = event_routes[event][0]
            #process as AI
            await think(
                event_routes[event][1],
                event_d
            )
            #Process as Slack/App
            return await handler(event_d)
