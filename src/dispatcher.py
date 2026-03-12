import json

from .handlers.ping import reply

def challenge_verif(data):
    return {"challenge": data["challenge"]}

def message(data):
    return reply(data)

event_routes = {
     "url_verification": challenge_verif,
     "event_callback":{
         "message":message,
         "mention":message
     }
}

def event_dispatch(type,data):
    if type == "url_verification":
        return event_routes[type](data)
    elif type == "event_callback":
        event_d = data.get("event")
        event = event_d["type"]
        
        if event in event_routes[types]:
            return event_routes[type][event](event_d)
