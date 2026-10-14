import json
from fastapi import APIRouter, Request

from .dispatcher import event_dispatch
from .globals import return_s_secret
from .redis import check
from .security.json import checkjson
from .security.traffic_in import verify_slack_signature

router = APIRouter()

#Routing events
@router.post("/slack/events")
async def slack_events(request: Request):
    #We will handle this differently
    """
    -We verify that the data is ok
    -Check if comes from slack
    -Redis will check if the received
    data is not duplicated
    -Once all of the above is ok
    -Dispatcher will handle everything
    else. :P
    """

    await verify_slack_signature(
        request,
        return_s_secret()
    )
    
    try:
        payload = json.loads(
            (await request.body()).decode("utf-8")
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="invalid json")

    checkjson(payload)
    
    if payload.get("type") == "url_verification":
       return {"challenge": payload["challenge"]}

    """
    key is made from the event 
    and timestamp, prevents
    duplicated slack events
    """
    #To-Do: Handle this better, like
    #checking if the data exist
    
    #Add everything else

    event_type = payload.get("event").get("type")
    ts = payload.get("event").get("ts")
    key = "key:"+event_type+":"+ts

    if await check(key):
        return await event_dispatch(payload)
    else:
        return {"status": "ok"}
    
    #Context code here, idk, maybe useful

    #Another and better logger here, maybe
    return {"status": "ok"}

"""
Cron job from cron-job.org here to maintain
redis alive :>

Or any cronjob request, like notifications,

allat here :>
"""

#Railway needs this, for some reason
@router.get("/health")
async def health():
    return {"status": "ok"}  
# simple healthcheck for deployment probes
