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
    #print(chat)
    test = f"
    data is: {persona["traits"]} and :)
    "
    print(persona)
    print(test)
    messages=[
        {
            "role": "user", 
            "content": "hello"
        }
    ]
    return messages
