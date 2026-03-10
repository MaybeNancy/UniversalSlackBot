#services
# src/services.py
import os, httpx

class SlackService:
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.client = httpx.AsyncClient(timeout=10)

    async def post_message(self, channel: str, text: str):
        await self.client.post(
            "https://slack.com/api/chat.postMessage",
            json={"channel": channel, "text": text},
            headers={"Authorization": f"Bearer {self.bot_token}"},
        )
