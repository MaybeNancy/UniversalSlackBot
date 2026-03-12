def test():
    printf("hello")

def message():
    printf("hello")

event_routes = {
    "0":test,
    "1":message
}

def event_dispatch(event,data):
    d[event](data)
