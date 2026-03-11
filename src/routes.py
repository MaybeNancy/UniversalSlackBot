import hmac, hashlib, json, time
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from src.tasks.background import run_in_background
from src.context import Context

router = APIRouter()

#Slack signature, we nees to simplify this
def verify_signature(request: Request, body: bytes, signing_secret: str):
    # Read Slack headers required for verification
    ts = request.headers.get("X-Slack-Request-Timestamp")
    sig = request.headers.get("X-Slack-Signature")
    if not ts or not sig:
        raise HTTPException(400, "Missing Slack headers")

    # Ensure timestamp is an integer and not too old (prevents replay attacks)
    try:
        ts_i = int(ts)
    except Exception:
        raise HTTPException(400, "Invalid timestamp")
    if abs(time.time() - ts_i) > 300:
        raise HTTPException(400, "Stale request timestamp")

    # Build Slack's signing base string and compute HMAC using the signing secret
    basestring = f"v0:{ts}:{body.decode()}"
    my_sig = "v0=" + hmac.new(
        signing_secret.encode(),
        basestring.encode(),
        hashlib.sha256,
    ).hexdigest()

    # Constant-time compare to prevent timing attacks
    if not hmac.compare_digest(my_sig, sig):
        raise HTTPException(403, "Invalid Slack signature")

#Routing events
@router.post("/slack/events")
async def slack_events(request: Request, background: BackgroundTasks):
    #We will handle this differently
    raw = await request.body()                   # read raw bytes for signature verification
    slack = request.app.state.slack              # get SlackService created at startup
    verify_signature(request, raw, slack.signing_secret)  # raises HTTPException on failure
    payload = json.loads(raw)                    # parse Slack event JSON

    # URL verification flow (Slack requires synchronous challenge response)
    if payload.get("type") == "url_verification":
        return {"challenge": payload["challenge"]}

    #I don't even know what is this
    ctx = Context(
        slack=slack,
        semaphore=request.app.state.semaphore,
    )

    #I don't think we need this, maybe not like this
    try:
        ctx.logger = slack.logger
    except Exception:
        pass

    # Schedule background processing so request returns quickly
    background.add_task(run_in_background, ctx, payload)
    return {"ok": True}

#Railway needs this, for some reason
@router.get("/health")
async def health():
    return {"status": "ok"}  # simple healthcheck for deployment probes
