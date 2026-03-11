## CODE GOALS:
- Use async (in progress)
- No critical data stored in files or memory (all credentials for app auth are handled elsewhere, anything else is no critical)
- Small independent modules
- Background jobs (in progress)
- Fewer dependencies
    

###CORE COMPONENTS:
-FastAPI
-Dispatcher/Router (to be modified)
-Handlers and plugins (to be modified)
-Services/Integrations (kinda added)
-Storage [tiny json files/in memory data] (not needed right now, but possibly in a future
-Caching (LRU /TTL) (To be added)
-Rate limiter (Kinda added)
-Background tasks / in progress (async stuff) (kinda added)
-Concurrency thingy (Semaphore, kinda added)
-Logging

###EXTRA:
-Built in logger, so I can catch bugs with the app itself
-Health endpoint (kinda added)
-Schema validation (to be modified)
-Slack block attachment formatting util (to be added)
-Error handling/signature verification (to be modified)
-Ack Slack inmediately (to be modified)
        
AND MUCH MORE!!! (Eventually added :>)
