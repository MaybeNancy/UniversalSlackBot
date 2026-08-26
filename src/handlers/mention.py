"""
I will modify this later, 
I just need the thing working
"""
import asyncio

from ..services.slack import send_message, new_name, get_user
from ..services.ai import call_ai

from ..utils.nancyfy import nancyfy

async def reply(data):
    # Example handler: respond "pong" when bot is mentioned
    #await new_name()
    #try:
    
   # except:
        #print("not working now")
    print(await get_user(data.get("user")))
    text = data["text"]
    prompt = "Someone said to you the following: "+text
    channel = data["channel"]
    ai = str(call_ai(prompt))
    response = nancyfy(ai)
    return await send_message(channel, ai)
    # Use ctx.logger if present; fallback to ctx.slack.logger
