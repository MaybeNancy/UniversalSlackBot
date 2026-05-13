import httpx, json, asyncio

from ..globals import return_client, return_b_token
from .httpx import post

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
    data = {
        "channel": channel, 
        "text": txt,
        "username":"Assistant🤖 (Brian)"
    }
    return await post(
        BASE_URL+"chat.postMessage",
        BASE_HEAD,
        data
    ).json()

#fix this later
async def new_name():
    data = {
        "profile":{
            "display_name":"Assistant",
            "display_name_normalized":"assistant"
        }
    }
    return await post(
        BASE_URL+"users.profile.set",
        BASE_HEAD,
        data
    ).json()
