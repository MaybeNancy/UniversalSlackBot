import hmac, hashlib, json, time
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
#from src.tasks.background import run_in_background

from .dispatcher import event_dispatch
from .services.slack_service import SLACK_SECRET

router = APIRouter()

#Slack signature, we need to simplify this
def verify_signature(request, signing_secret):
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    slack_signature = request.headers.get("X-Slack-Signature", "")
    if not timestamp or not slack_signature:
        abort(401)

    # Reject if timestamp is too old (5 minutes)
    try:
        req_ts = int(timestamp)
    except ValueError:
        abort(401)
    if abs(time.time() - req_ts) > 60 * 5:
        abort(401)

    # Get raw body bytes exactly as received
    body_bytes = request.get_data()  # bytes
    basestring = f"v0:{timestamp}:{body_bytes.decode('utf-8', 'surrogatepass')}"
    sig_basestring = basestring.encode("utf-8")

    my_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring,
        hashlib.sha256
    ).hexdigest()

    if not compare_digest(my_signature, slack_signature):
        abort(401)
    # verified

#Routing events
@router.post("/slack/events")
def slack_events(request: Request, background: BackgroundTasks):
    #We will handle this differently
    """
    -We verify that the data is ok
    -Check if comes from slack
    -Dispatcher will handle everything
    else. :P
    """
    
    verify_signature(request, SLACK_SECRET)  # raises HTTPException on failure
    payload = json.loads(raw)                    # parse Slack event JSON

    return event_dispatch(payload.get("type"),payload)
    # URL verification flow (Slack requires synchronous challenge response)
    
    #if payload.get("type") == "url_verification":
        #return {"challenge": payload["challenge"]}

    #Context code here, idk, maybe useful
    
    #Another and better logger here, maybe

    #Background schedule proccessing thingy
    
    #We need more info on this:
    #return {"ok": True}

#Railway needs this, for some reason
@router.get("/health")
def health():
    return {"status": "ok"}  # simple healthcheck for deployment probes
