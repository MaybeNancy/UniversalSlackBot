import json

import handlers.ping

def challenge_verif(data):
    return {"challenge": data[challenge]}

def message(data):
    return reply(data)

event_routes = {
    "url_verification":challenge_verif,
    "message":message
}

def event_dispatch(event,data):
    #try error catching later
   return event_routes[event](data)
