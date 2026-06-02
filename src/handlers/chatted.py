import asyncio

from ..services.slack import edit_message

from ..utils.nancyfy import nancyfy

async def emojify(data):
    channel = data["channel"]
    text = nancyfy(data["text"])
    return await send_message(channel, text)
