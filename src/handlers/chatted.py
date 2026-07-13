import asyncio, random

from ..services.slack import react
from ..services.ai import call_ai

from ..utils.nancyfy import nancymoji

async def emojify(data):
    channel = data["channel"]
    ts = data["ts"]
    return await react(channel, nancymoji(),ts)

async def talk(data):
    
    channel = data["channel"]
    user = data["user"]
    text = data["text"]
    prompt="Say hello to "+str(user)
    print(user)
    text = str(call_ai(prompt))
    return await send_message(channel, text)

async def get_message(data):
    r = random.randint(1,3)
    if(r == 1):
        return await emojify(data)
    if(r>=1):
        return await talk(data)
    
    return {"status":"ok"}
