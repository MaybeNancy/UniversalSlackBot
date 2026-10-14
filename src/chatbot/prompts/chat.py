"""
Code that builds the messages
parameter properly for the ai to
use for chatting

"user", "assistant", "system"
"""
import asyncio
from ...services.slack import get_chat

async def respond(persona, data):
    chat = await get_chat(data["channel"])
    print(chat)
    print(persona)
    messages=[
        {
            "role": "user", 
            "content": "hello"
        }
    ]
    return messages
