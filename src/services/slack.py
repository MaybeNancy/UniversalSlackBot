import json, asyncio

from ..globals import return_client, return_b_token
from .shttpx import spost

BASE_URL = "https://slack.com/api/"

BASE_HEAD={
            "Authorization": f"Bearer {return_b_token()}",
            "Content-Type": "application/json; charset=utf-8"
        }
"""
Still needs improvements, but
is a start :P
"""

async def send_message(channel, txt):
    res = await post(
        BASE_URL+"chat.postMessage",
        BASE_HEAD,
        {
            "channel": channel, 
            "text": txt,
            "username":"Assistant🤖 (Brian)"
        }
    )
    print(res)
    return res.json()
    

#fix this later
async def new_name():
    return await post(
        BASE_URL+"users.profile.set",
        BASE_HEAD,
        {
            "profile":{
                "display_name":"Assistant",
                "display_name_normalized":"assistant"
            }
        }
    ).json()
