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
    prompt="Say hello to Nancy"
    print(s_user)
    print(await get_user(s_user))
    text = str(call_ai(prompt))
    return await send_message(channel, text)

async def get_message(data):
    r = random.randint(1,3)
    if(r == 1):
        await emojify(data)
    if(r>=1):
        await talk(data)
    
    return {"status":"ok"}
