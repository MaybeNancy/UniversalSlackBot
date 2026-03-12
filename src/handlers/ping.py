"""
I will modify this later, 
I just need the thing working
"""
import asyncio

from ..services.slack_service import send_message

async def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    channel = data["channel"]
    return await send_message(channel, "Hey")
    # Use ctx.logger if present; fallback to ctx.slack.logger
