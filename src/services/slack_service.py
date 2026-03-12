import os, httpx, json, asyncio

from ..globals import return_client

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")

"""
Still needs improvements, but
is a start :P
"""

def send_message(channel, txt):
    url = "https://slack.com/api/chat.postMessage"
    
    headers={"Authorization": f"Bearer {BOT_TOKEN}"}
    
    data = {
        "channel": channel, 
        "text": txt
    }
    
    client = return_client()
    resp = client.post(
            url,
            json=data,
            headers=headers
        )
    
    return resp.json()
