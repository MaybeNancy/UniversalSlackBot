# src/routes.py
import hmac, hashlib, json
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from src.services import SlackService
from src.storage import FileStore

router = APIRouter()
slack = SlackService()
store = FileStore("data")

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

    # -------------------------------------------------
    # 1️⃣  URL verification – reply **immediately**
    # -------------------------------------------------
    if payload.get("type") == "url_verification":
        # Slack expects exactly this JSON object
        return {"challenge": payload["challenge"]}

    # -------------------------------------------------
    # 2️⃣  Normal events – ACK quickly, process async
    # -------------------------------------------------
    background.add_task(handle_payload, payload)
    return {"ok": True}


# ----------------------------------------------------------------------
# Background worker – runs after the ACK
# ----------------------------------------------------------------------
async def handle_payload(payload: dict):
    dispatcher = request.app.state.dispatcher
    await dispatcher.dispatch(payload, slack, store)
