# src/services/slack_service.py
import os, httpx
from src.utils.logging import get_logger

class SlackService:
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.client = httpx.AsyncClient(timeout=10)
        self.logger = get_logger("slack")
        # keep a back‑reference to the FastAPI app for Context convenience
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
        if not data.get("ok"):
            self.logger.error("Slack postMessage failed", response=data)
        return data

    # Lazy creation of other services – keeps imports cheap
    async def get_openai_service(self):
        from src.services.openai_service import OpenAIService
        return OpenAIService()
