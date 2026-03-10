#this patch
# src/dispatcher.py
import importlib
import pkgutil
from typing import Callable, Awaitable

Handler = Callable[[dict, "SlackService", "FileStore"], Awaitable[None]]

class Dispatcher:
    def __init__(self):
        self.handlers: dict[str, Handler] = {}
        self._load_handlers()

    def _load_handlers(self):
        # import every module in src.handlers and call its register()
        pkg = importlib.import_module("src.handlers")
        for _, name, _ in pkgutil.iter_modules(pkg.__path__):
            mod = importlib.import_module(f"src.handlers.{name}")
            if hasattr(mod, "register"):
                mod.register(self)

    def register(self, event_type: str, handler: Handler):
        self.handlers[event_type] = handler

    async def dispatch(self, payload: dict, slack, store):
        # Slack sends either a top‑level "type" (url_verification) or an
        # inner "event.type".  We care about the latter.
        event_type = payload.get("event", {}).get("type")
        if not event_type:
            return  # nothing we handle

        handler = self.handlers.get(event_type)
        if handler:
            await handler(payload, slack, store)
