"""
Code that creates a prompt
telling the bot to select a
reaction based on context and
mood
"""

from ..emojis import nancymoji

async def emojify(data):
    channel = data["channel"]
    ts = data["ts"]
    return await react(channel, nancymoji(),ts)
