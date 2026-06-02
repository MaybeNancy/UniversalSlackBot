import asyncio, random

from ..services.slack import react

from ..utils.nancyfy import nancymoji

async def emojify(data):
    if(random.randint(1,3) == 1):
        channel = data["channel"]
        ts = data["ts"]
        return await react(channel, nancymoji(),ts)
    else:
        return {"status": "ok"}
