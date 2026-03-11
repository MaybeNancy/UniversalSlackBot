# src/dispatcher.py
import importlib, pkgutil
from typing import Callable, Awaitable, Dict
from src.context import Context

Handler = Callable[[Context, dict], Awaitable[None]]

class Dispatcher:
    def __init__(self):
        self._registry: Dict[str, Handler] = {}
        self._load_handlers()

    def _load_handlers(self):
        """Import every module under src.handlers and call its register()."""
        pkg = importlib.import_module("src.handlers")
        for _, name, _ in pkgutil.iter_modules(pkg.__path__):
            mod = importlib.import_module(f"src.handlers.{name}")
            if hasattr(mod, "register"):
                mod.register(self)

    def register(self, event_type: str, handler: Handler):
        self._registry[event_type] = handler

    async def dispatch(self, ctx: Context, payload: dict):
        # Slack events are nested under "event"
        event_type = payload.get("event", {}).get("type")
        if not event_type:
            ctx.logger.debug("Payload without event.type", payload=payload)
            return

        handler = self._registry.get(event_type)
        if handler:
            await handler(ctx, payload)
        else:
            ctx.logger.info("No handler for event", event_type=event_type)
