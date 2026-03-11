import importlib, pkgutil, inspect
from typing import Callable, Awaitable, Dict
from src.context import Context

# Handler type: async callable accepting (Context, payload)
Handler = Callable[[Context, dict], Awaitable[None]]

class Dispatcher:
    def __init__(self):
        self._registry: Dict[str, Handler] = {}  # maps Slack event.type -> handler
        self._load_handlers()                     # import and register handlers on creation

    def _load_handlers(self):
        # Dynamically import each module in src.handlers and call its register(self)
        pkg = importlib.import_module("src.handlers")
        for _, name, _ in pkgutil.iter_modules(pkg.__path__):
            mod = importlib.import_module(f"src.handlers.{name}")
            if hasattr(mod, "register"):
                mod.register(self)

    def register(self, event_type: str, handler: Handler):
        # Register a handler for a Slack event type (overwrites if duplicate)
        self._registry[event_type] = handler

    async def dispatch(self, ctx: Context, payload: dict):
        # Extract Slack event type (events are under payload["event"]["type"])
        event_type = payload.get("event", {}).get("type")
        if not event_type:
            return  # nothing to do

        handler = self._registry.get(event_type)
        if not handler:
            return  # no handler registered for this event type

        try:
            # Call the handler; support both async callables and callables returning awaitables
            result = handler(ctx, payload)
            if inspect.isawaitable(result):
                await result
        except Exception:
            # Log exceptions from handlers but don't let them crash the background task
            try:
                # ctx.logger expected to exist (attached in routes startup). Fallback to slack.logger.
                if hasattr(ctx, "logger"):
                    ctx.logger.exception("handler failed", event_type=event_type)
                elif hasattr(ctx.slack, "logger"):
                    ctx.slack.logger.exception("handler failed", event_type=event_type)
            except Exception:
                # If logger is missing, swallow to avoid secondary errors
                pass
