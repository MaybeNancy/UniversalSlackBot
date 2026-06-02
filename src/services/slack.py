import json, asyncio

from ..globals import return_client, return_b_token
from .shttpx import spost

BASE_URL = "https://slack.com/api/"

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
            "username":"Assistant🤖 (Brian)"
        }
    )
    print(BASE_HEAD)
    return res.json()
    

#fix this later
async def new_name():
    return await post(
        BASE_URL+"users.profile.set",
        head_type(return_b_token()),,
        {
            "profile":{
                "display_name":"Assistant",
                "display_name_normalized":"assistant"
            }
        }
    ).json()
