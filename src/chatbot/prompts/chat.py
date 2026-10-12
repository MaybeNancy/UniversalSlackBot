"""
Code that builds the messages
parameter properly for the ai to
use for chatting

"user", "assistant", "system"
"""
import asyncio
from ...services.slack import get_chat

async def lookchat():
    chat = await get_chat()
    messages=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
    return messages
