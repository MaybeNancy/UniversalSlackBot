import json

import handlers.ping

def challenge_verif(data):
    return {"challenge": data[challenge]}

def message():
    return {"status":"ok"}

event_routes = {
    "url_verification":challenge_verif,
    "message":message
}

def event_dispatch(event,data):
    #try error catching later
   return event_routes[event](data)
