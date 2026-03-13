import os, httpx, json, asyncio

from ..globals import return_client

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")
BASE_URL = "https://slack.com/api/"

"""
Still needs improvements, but
is a start :P
"""

async def send_message(channel, txt):
    url = BASE_URL+"chat.postMessage"
    
    headers={
        "Authorization": f"Bearer {BOT_TOKEN}"
    }
    
    data = {
        "channel": channel, 
        "text": txt,
        "username":"Assistant🤖"
    }
    
    client = return_client()
    resp = await client.post(
            url,
            json=data,
            headers=headers
    )
    
    return resp.json()

#modify thi later
async def new_name():
    url = BASE_URL+"users.profile.set"
    headers = {
        "Authorization": f"Bearer {BOT_TOKEN}"
    }
    data = {
        
    }
  
    client = return_client()
    resp = await client.post(
            url,
            json=data,
            headers=headers
        )
    
    return resp.json()
