import os, httpx

class SlackService:
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.client = httpx.AsyncClient(timeout=10)
        self._fastapi_app = None

    async def post_message(self, channel: str, text: str, blocks=None):
        payload = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks
        resp = await self.client.post(
            "https://slack.com/api/chat.postMessage",
            json=payload,
            headers={"Authorization": f"Bearer {self.bot_token}"},
        )
        data = resp.json()
        return data
