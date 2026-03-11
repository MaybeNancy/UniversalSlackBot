# src/routes.py
import hmac, hashlib, json
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from src.services.slack_service import SlackService
from src.storage.file_store import FileStore
from src.tasks.background import run_in_background
from src.context import Context

router = APIRouter()
slack = SlackService()                     # reads env vars
store = FileStore(base_path="data/file_store")

def verify_signature(request: Request, body: bytes):
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
    verify_signature(request, raw)
    payload = json.loads(raw)

    # URL verification – must be answered synchronously
    if payload.get("type") == "url_verification":
        return {"challenge": payload["challenge"]}

    # ACK quickly, then process the event in the background
    ctx = Context(
        slack=slack,
        openai=await slack.get_openai_service(),
        storage=store,
        logger=slack.logger,
        semaphore=request.app.state.semaphore,
    )
    background.add_task(run_in_background, ctx, payload)
    return {"ok": True}

@router.get("/health")
async def health():
    return {"status": "ok"}
