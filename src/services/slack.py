import json, asyncio

from ..globals import return_client, return_b_token
from .shttpx import spost

BASE_URL = "https://slack.com/api/"
BOT_BASE_NAME = "Brian The SlackBot🤖 (AKA: Assistant)"

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

async def get_user(s_user):
    res = await spost(
        BASE_URL+"users.info",
        head_type(return_b_token()),
        {
            "user": s_user
        }
    )
    return res.json()

#fix this later
async def new_name():
    return await post(
        BASE_URL+"users.profile.set",
        head_type(return_b_token()),
        {
            "profile":{
                "display_name":"Assistant",
                "display_name_normalized":"assistant"
            }
        }
    ).json()
