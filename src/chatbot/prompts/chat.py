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
    #print(chat)

    prompt = (
        f"{persona}, "
        f"and you're talking in a chat room/server, "
        f"like talking to someone face to face in 1st person, "
        f"avoid writing like describing/telling a story, "
        f"add a short but worth-reading response to the conversation"
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
            user = ""
            
            if "user" in p:
                name = await get_user_name(p["user"])
                if name != False:
                    role = "user"
                    user = f"[{name}]: "
                else:
                    user = ""
                    
            new_mssg = {
                "role":role,
                "content":f'{user}{p["text"]}'
            }
            messages.append(new_mssg)
    
        return messages
    return False
