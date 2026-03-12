import json

from .handlers.ping import reply

def challenge_verif(data):
    return {"challenge": data["challenge"]}

def message(data):
    return reply(data)

event_routes = {
     "url_verification": challenge_verif,
     "event_talkback":{
         "message":message,
         "mention":message
     }
}

def event_dispatch(type,data):
    if type == "url_verification":
        return event_routes[type](data)
    else
    
        event_d = data.get("event")
        return event_routes[type][event_d["type"]](event_d)
