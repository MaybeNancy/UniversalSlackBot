import asyncio, random

from ..services.slack import react
from ..services.ai import call_ai

from ..utils.nancyfy import nancymoji

async def emojify(data):
    channel = data["channel"]
    ts = data["ts"]
    return await react(channel, nancymoji(),ts)

async def talk(data):
    return {"status":"ok"}

async def get_message(data):
    r = random.randint(1,3)
    if(r == 1):
        return emojify(data)
    elif(r>1):
        return talk(data)
    else:
        return {"status":"ok"}
        
