import os, httpx

import globals

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")

"""
We don't need oop for this,
the only good thing is the post message
function, We need to tweak this.
"""

def send_message(channel, txt):
    url = "https://slack.com/api/chat.postMessage"
    
    headers={"Authorization": f"Bearer {self.bot_token}"}
    
    data = {
        "channel": channel, 
        "text": text
    }

    resp = await self.client.post(
            url,
            json=data,
            headers=headers
        )
    return resp.json()

    async def post_message(self, channel: str, text: str, blocks=None):
        # Send chat.postMessage to Slack using the bot token
        
        if blocks:
            payload["blocks"] = blocks
        
        data = resp.json()  # parse Slack response JSON
        return data
