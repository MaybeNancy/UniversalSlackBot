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
        f", and you're in a chat room/server, so avoid adding story"
        f"just add a plain text response to the following conversation"
    )
    messages=[
        {
            "role":"system",
            "content":prompt
        }
    ]

    if "messages" in chat:
        for p in reversed(chat["messages"]):
            role = "assistant"
            
            if "user" in p:
                user = await get_user_name(p["user"])
                if user != False:
                   role = "user"
                else:
                    user = ""

            new_mssg = {
                "role":role,
                "content":f"[{user}]: {p["text"]}"
            }
            messages.append(new_mssg)
    
    return messages
