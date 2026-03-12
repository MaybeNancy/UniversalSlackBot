import os, httpx

from ..globals import return_client

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")

"""
Still needs improvements, but
is a start :P
"""

def send_message(channel, txt):
    url = "https://slack.com/api/chat.postMessage"
    
    headers={"Authorization": f"Bearer {self.bot_token}"}
    
    data = {
        "channel": channel, 
        "text": text
    }
    
    client = return_client()
    resp = client.post(
            url,
            json=data,
            headers=headers
        )
    
    return resp.json()
