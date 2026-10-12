"""
Handles and verifies the legitimacy
of any data that other public 
endpoints sends
to the app, preventing
the app from dealing with
unauthorized/malicious traffic
"""

import hmac, hashlib, json, time, asyncio
from hmac import compare_digest
from fastapi import Request, HTTPException

def verify_signature(
  timestamp,
  signature,
  request, 
  signing_secret, 
  body_bytes
):
    if not timestamp or not signature:
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

    if not compare_digest(my_signature, signature):
        raise HTTPException(status_code=401, detail="invalid signature")
    # verified

#Slack signature, we need to check this
async def verify_slack_signature(request, signing_secret):
    verify_signature(
        request.headers.get("X-Slack-Request-Timestamp", ""),
        request.headers.get("X-Slack-Signature", ""),
      
        request,
        signing_secret,
        await request.body()
    )
