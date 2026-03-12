def challenge_verif(data):
    return {"challenge": data[challenge]}

def message():
    print("hello")

event_routes = {
    "url_verification":challenge_verif,
    "message":message
}

def event_dispatch(event,data):
   return event_routes.get(event)
