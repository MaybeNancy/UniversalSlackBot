"""
Code that builds the messages
parameter properly for the ai to
use for chatting

"user", "assistant", "system"
"""
import asyncio
from ...services.slack import get_chat, get_user_name

async def respond(persona, data):
    chat = await get_chat(data["channel"])
    print(chat)

    prompt = (
        f"{persona}, "
        f"add something short to the conversation"
    )
    messages=[
        {
            "role":"system",
            "content":prompt
        },
        {
            "role": "user", 
            "content": "hello"
        }
    ]

    if "members" in chat:
        for p in chat["members"]:
            user = get_user_name(p["user"])
            messages.update(
                {
                    "role":"user",
                    "content":f"'{user}': {p["text"]}"
                }
            )
    
    return messages
