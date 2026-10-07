import json, asyncio

from ..globals import return_client, return_b_token
from .shttpx import spost
from ..utils.roleplay import CHARS, char_list

BASE_URL = "https://slack.com/api/"
BOT_BASE_NAME = CHARS[char_list[0]]["name"]
PAGE_LENGTH = 50

def head_type(token):
    base_head={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8"
            }
    return base_head
"""
Still needs improvements, but
is a start :P
"""

async def send_message(channel, txt):
    res = await spost(
        BASE_URL+"chat.postMessage",
        head_type(return_b_token()),
        {
            "channel": channel, 
            "text": txt,
            "username":BOT_BASE_NAME
        }
    )
    return res.json()

async def send_ghostly(channel,user,txt):
    res = await spost(
        BASE_URL+"chat.postEphemeral",
        head_type(return_b_token()),
        {
            "channel": channel, 
            "user": user,
            #"icon_url": icon,
            "text": txt+" (Ghostly! 👻)",
            "username":BOT_BASE_NAME
        }
    )
    return res.json()

async def react(channel,emoji,ts):
    res = await spost(
        BASE_URL+"reactions.add",
        head_type(return_b_token()),
        {
            "channel": channel, 
            "name": emoji,
            "timestamp":ts
        }
    )
    return res.json()

async def get_all_users(pcursor, id):
    print("cursor =",cursor)
    cursor = pcursor
    users_page = await spost(
        BASE_URL+"users.list",
        head_type(return_b_token()),
        {
            "cursor":cursor
            "limit":PAGE_LENGTH
        }
    )

    for u in users_page["members"]:
        print(u["id"])
        if u["id"] == id:
              if "display_name" in u["profile"]:
                  return u["profile"]["display_name"]
              else:
                  return u["real_name"]

    if user_page.get("response_metadata") not None:
        metadata = user_page.get("response_metadata")
        if metadata.get("next_cursor") not None:
            cursor = metadata.get("next_cursor")
            if cursor not "":
                return await get_all_users(cursor, id)
    
    return "Unknown"

async def get_user_name(id):
    cursor = ""
    return await get_all_users(cursor, id)

#fix this later
async def new_name():
    res = await spost(
        BASE_URL+"users.profile.set",
        head_type(return_b_token()),
        {
            "profile":{
                "display_name":"Assistant",
                "display_name_normalized":"assistant"
            }
        }
    )
    return res.json()
