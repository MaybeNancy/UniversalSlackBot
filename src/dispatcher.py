import json

from .handlers.ping import reply

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
    
    ##quick fix, delete later
   #return event_routes[event](data)
    return message(data)
