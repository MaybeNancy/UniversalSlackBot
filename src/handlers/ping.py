"""
I will modify this later, 
I just need the thing working
"""
import asyncio

from ..services.slack import send_message, new_name
from ..services.perchance import call_site

async def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    #await new_name()
    ptxt=await call_site()
    print("Slack callin'")
    channel = data["channel"]
    text = "Hello! new me, new everything, work in progress, comeback later :nancy-wink:"
    return await send_message(channel, text)
    # Use ctx.logger if present; fallback to ctx.slack.logger
