def test():
    print("hello")

def message():
    print("hello")

event_routes = {
    "0":test,
    "1":message
}

def event_dispatch(event,data):
    event_routes.get(event)
