"""
I will modify this later, 
I just need the thing working
"""
import asyncio

from ..services.slack import send_message, new_name
from ..services.ai import call_ai

async def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    #await new_name()
    #try:
    
   # except:
        #print("not working now")
    txt="Write a short and lovely horror story staring Nancy"
    channel = data["channel"]
    text = str(call_ai(txt))+":nancy-scream::candle-pumpkin"
    return await send_message(channel, text)
    # Use ctx.logger if present; fallback to ctx.slack.logger
