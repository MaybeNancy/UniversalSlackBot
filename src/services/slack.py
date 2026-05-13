import httpx, json, asyncio

from ..globals import return_client, return_b_token

BASE_URL = "https://slack.com/api/"

headers={
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
    
    return await slack_action("chat.postMessage",None,data)

#modify thi later
async def new_name():
    data = {
        "profile":{
            "display_name":"Assistant",
            "display_name_normalized":"assistant"
        }
    }
    return await post.json()
    return await slack_action("users.profile.set",None,data)
