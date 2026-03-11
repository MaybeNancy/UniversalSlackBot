import hmac, hashlib, json, time
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from src.tasks.background import run_in_background
from src.context import Context

router = APIRouter()

def verify_signature(request: Request, body: bytes, signing_secret: str):
    ts = request.headers.get("X-Slack-Request-Timestamp")
    sig = request.headers.get("X-Slack-Signature")
    if not ts or not sig:
        raise HTTPException(400, "Missing Slack headers")
    try:
        ts_i = int(ts)
    except Exception:
        raise HTTPException(400, "Invalid timestamp")
    if abs(time.time() - ts_i) > 300:
        raise HTTPException(400, "Stale request timestamp")
    basestring = f"v0:{ts}:{body.decode()}"
    my_sig = "v0=" + hmac.new(
        signing_secret.encode(),
        basestring.encode(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(my_sig, sig):
        raise HTTPException(403, "Invalid Slack signature")

@router.post("/slack/events")
async def slack_events(request: Request, background: BackgroundTasks):
    raw = await request.body()
    slack = request.app.state.slack
    verify_signature(request, raw, slack.signing_secret)
    payload = json.loads(raw)

    if payload.get("type") == "url_verification":
        return {"challenge": payload["challenge"]}

    ctx = Context(
        slack=slack,
        semaphore=request.app.state.semaphore,
    )
    background.add_task(run_in_background, ctx, payload)
    return {"ok": True}

@router.get("/health")
async def health():
    return {"status": "ok"}
