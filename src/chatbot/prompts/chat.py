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

    prompt = (
        f"{persona}, "
        f", and you're chatting, so avoid adding story"
        f" verbs and all of that,"
        f"just add a response/text to the following conversation"
    )
    messages=[
        {
            "role":"system",
            "content":prompt
        }
    ]

    if "messages" in chat:
        for p in reversed(chat["messages"]):
            role = "user"
            user = ""
            if "user" in p:
                user = await get_user_name(p["user"])
            else:
                role = "assistant"
            new_mssg = {
                "role":role,
                "content":f"'{user}': {p["text"]}"
            }
            messages.append(new_mssg)
    
    return messages
