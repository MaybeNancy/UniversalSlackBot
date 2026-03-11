import os, httpx

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SECRET = os.getenv("SLACK_SIGNING_SECRET")

"""
We don't need oop for this,
the only good thing is the post message
function, We need to tweak this.
"""
class SlackService:
    def __init__(self):
        # Read credentials from environment variables (set these in Railway)
        # Reusable async HTTP client for Slack API calls
        self.client = httpx.AsyncClient(timeout=10)
        # Back-reference to FastAPI app (set in startup) so Context.app can access app.state
        self._fastapi_app = None
        # Logger will be attached at app startup: app.state.slack.logger = get_logger(...)
        self.logger = None

    async def post_message(self, channel: str, text: str, blocks=None):
        # Send chat.postMessage to Slack using the bot token
        payload = {"channel": channel, "text": text}
        if blocks:
            payload["blocks"] = blocks
        resp = await self.client.post(
            "https://slack.com/api/chat.postMessage",
            json=payload,
            headers={"Authorization": f"Bearer {self.bot_token}"},
        )
        data = resp.json()  # parse Slack response JSON
        return data
