## CODE GOALS:
- Use async (Done? I guess)
- No critical data stored in files or memory (all credentials for app auth are handled elsewhere, anything else is no critical)
- Small independent modules
- REDIS
- Fewer dependencies
    

## CORE COMPONENTS:
- FastAPI
- Dispatcher/Router (simplified)
- Handlers and plugins (to be modified more)
- Services/Integrations (kinda added)
- Storage [tiny json files/in memory data] (not needed right now, but possibly in a future)
- REDIS THINGY: (To be added)
  - Rate limiter
  - Offload tasks (async stuff)
  - Concurrency thingy
  - Caching (LRU /TTL) (To be added)
- Logging

## EXTRA:
- Built in logger, so I can catch bugs with the app itself
- Health endpoint (kinda added)
- Schema validation (better but still needa checks)
- Slack block attachment formatting util (to be added)
- Error handling/signature verification (to be modified)
- Ack Slack inmediately (to be improved with the help of REDIS)
        
> AND MUCH MORE!!! (Eventually added **:>**)

> [!WARNING]
> Project is under critical modifications, prone to errors, thank you for your patience **:'P**
