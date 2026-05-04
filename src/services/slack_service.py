import httpx, json, asyncio

from ..globals import return_client, return_b_token

BASE_URL = "https://slack.com/api/"

"""
Still needs improvements, but
is a start :P
"""

async def slack_action(url_add,n_headers,n_data):
    url = BASE_URL+url_add

    if n_headers == None:
        headers={
            "Authorization": f"Bearer {return_b_token}"
        }
    else:
        headers=n_headers
    data = n_data
    
    client = return_client()
    resp = await client.post(
            url,
            json=data,
            headers=headers
    )
    
    return resp.json()

async def send_message(channel, txt):
    data = {
        "channel": channel, 
        "text": txt,
        "username":"Assistant🤖 (Brian)"
    }
    print("mess")
    return await slack_action("chat.postMessage",None,data)

#modify thi later
async def new_name():
    data = {
        "profile":{
            "display_name":"Assistant",
            "display_name_normalized":"assistant"
        }
    }
    return await slack_action("users.profile.set",None,data)
