import asyncio

from ..services.slack import edit_message

from ..utils.nancyfy import nancymoji

async def emojify(data):
    channel = data["channel"]
    channel = data["ts"]
    return await react(channel, nancymoji(),ts)
