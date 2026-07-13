"""
I will modify this later, 
I just need the thing working
"""
import asyncio

from ..services.slack import send_message, new_name
from ..services.ai import call_ai

from ..utils.nancyfy import nancyfy

async def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    #await new_name()
    #try:
    
   # except:
        #print("not working now")
    prompt="Write a short horror story staring Nancy"
    channel = data["channel"]
    text = str(call_ai(prompt))+" :nancy-scream: :candle-pumpkin:"
    text = nancyfy(text)
    return await send_message(channel, text)
    # Use ctx.logger if present; fallback to ctx.slack.logger
