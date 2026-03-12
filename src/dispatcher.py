def challenge_verif():
    print("hello")

def message():
    print("hello")

event_routes = {
    "url_verification":challenge_verif,
    "message":message
}

def event_dispatch(event,data):
    event_routes.get(event)
