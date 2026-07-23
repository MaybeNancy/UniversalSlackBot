import asyncio, random

from ..services.slack import react, send_message, get_user
from ..services.ai import call_ai

from ..utils.nancyfy import nancymoji

async def emojify(data):
    channel = data["channel"]
    ts = data["ts"]
    return await react(channel, nancymoji(),ts)

async def talk(data):
    channel = data["channel"]
    s_user = data["user"]
    text = data["text"]
    prompt="Someone said: "+text+", add something short to the conversation if needed"
    
    print(await get_user(s_user))
    print(data)
    text = str(call_ai(prompt))
    return await send_message(channel, text)

async def get_message(data):
    r = random.randint(1,5)
    if r > 3:
        return await emojify(data)
    elif r <= 1:
        return await talk(data)
    else:
        return {"status":"ok"}
