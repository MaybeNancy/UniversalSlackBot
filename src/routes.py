# src/routes.py
import hmac, hashlib, json
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from src.services import SlackService

router = APIRouter()
slack = SlackService()          # reads SLACK_BOT_TOKEN / SLACK_SIGNING_SECRET
store = FileStore("data")       # tiny JSON folder (created automatically)

def verify(request: Request, body: bytes):
    ts = request.headers.get("X-Slack-Request-Timestamp")
    sig = request.headers.get("X-Slack-Signature")
    if not ts or not sig:
        raise HTTPException(400, "Missing Slack headers")
    basestring = f"v0:{ts}:{body.decode()}"
    my_sig = "v0=" + hmac.new(
        slack.signing_secret.encode(),
        basestring.encode(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(my_sig, sig):
        raise HTTPException(403, "Invalid Slack signature")

@router.post("/slack/events")
async def slack_events(request: Request, background: BackgroundTasks):
    raw = await request.body()
    verify(request, raw)
    payload = json.loads(raw)

    # URL verification (Slack sends this once)
    if payload.get("type") == "url_verification":
        return {"challenge": payload["challenge"]}

    # ACK quickly, then process async
    background.add_task(handle_payload, payload)
    return {"ok": True}

@router.get("/health")
async def health():
    return {"status": "ok"}

# ----------------------------------------------------------------------
# Background worker – calls the dispatcher
async def handle_payload(payload: dict):
    dispatcher = request.app.state.dispatcher
    await dispatcher.dispatch(payload, slack, store)
