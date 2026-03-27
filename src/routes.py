#check the imports later
import hmac, hashlib, json, time
from hmac import compare_digest
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
#from src.tasks.background import run_in_background

from .dispatcher import event_dispatch
from .globals import return_s_secret
from .redis import cacheck_ ,cacheck_write

router = APIRouter()

#Slack signature, we need to check this
def verify_signature(request, signing_secret, body_bytes):
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    slack_signature = request.headers.get("X-Slack-Signature", "")
    if not timestamp or not slack_signature:
        raise HTTPException(status_code=401, detail="missing slack signature")

    # Reject if timestamp is too old (5 minutes)
    try:
        req_ts = int(timestamp)
    except ValueError:
        raise HTTPException(status_code=401, detail="invalid timestamp")
    if abs(time.time() - req_ts) > 60 * 5:
        raise HTTPException(status_code=401, detail="timestamp too old")
    
    sig_basestring = b"v0:" + timestamp.encode("utf-8") + b":" + body_bytes

    my_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring,
        hashlib.sha256
    ).hexdigest()

    if not compare_digest(my_signature, slack_signature):
        raise HTTPException(status_code=401, detail="invalid signature")
    # verified

#Routing events
@router.post("/slack/events")
async def slack_events(request: Request, background: BackgroundTasks):
    #We will handle this differently
    """
    -We verify that the data is ok
    -Check if comes from slack
    -Dispatcher will handle everything
    else. :P
    """
    body_bytes = await request.body()
    # raises HTTPException on failure
    verify_signature(request,return_s_secret,body_bytes)
    
    
    try:
        payload = json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="invalid json")
    
    if payload.get("type") == "url_verification":
       return {"challenge": payload["challenge"]}


    result = await event_dispatch(payload)
    # URL verification flow (Slack requires synchronous challenge response)
    
    #if payload.get("type") == "url_verification":
        #return {"challenge": payload["challenge"]}

    #Context code here, idk, maybe useful
    
    #Another and better logger here, maybe
    return result

#Railway needs this, for some reason
@router.get("/health")
async def health():
    return {"status": "ok"}  
# simple healthcheck for deployment probes
