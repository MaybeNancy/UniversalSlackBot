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

def event_dispatch(event,data):
    if event == "url_verification":
        return event_routes[event](data)
    else
        g_event = data.get("event")
        return event_routes[0][g_event](data)
