import asyncio, random

from ..services.slack import react, send_message, get_user_name, get_chat

async def talk(data):
    channel = data["channel"]
    s_user = data.get("user")
    username = await get_user_name(s_user)
    text = data["text"]
    txt1 = "You're a discord chatbot, the user "+username+" said: '"
    prompt=txt1+text+"', please say reply with something appropiate to that person"
    
    return await send_message(channel, "nancy-think")

async def get_message(data):
    print(await get_chat(data["channel"]))
    r = random.randint(0,7)
    if r >= 5:
        return await emojify(data)
    elif r == 0:
        return await talk(data)
    else:
        return {"status":"ok"}
