import asyncio, random

from ..services.slack import react, send_message, get_user_name
from ..services.ai import call_ai

from ..utils.nancyfy import nancymoji

async def emojify(data):
    channel = data["channel"]
    ts = data["ts"]
    return await react(channel, nancymoji(),ts)

async def talk(data):
    channel = data["channel"]
    s_user = data.get("user")
    user_name = get_user_name(s_user)
    text = data["text"]
    txt1 = "You're a discord bot, "+username+" said: '"
    prompt=txt1+text+"', please say hi and his/her name back"
    
   # print(await get_user(s_user))
    #print(data)
    text = str(call_ai(prompt))
    return await send_message(channel, text)

async def get_message(data):
    return await talk(data)
    r = random.randint(0,7)
    if r >= 5:
        return await emojify(data)
    elif r == 0:
        return await talk(data)
    else:
        return {"status":"ok"}
