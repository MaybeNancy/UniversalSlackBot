Railway URL: https://multitask-slack-bot.up.railway.app/slack/events

Netlify URL: https://multitask-slack-bot.netlify.app/.netlify/functions/handler/slack/events

CODE GOALS:
###################
Core principles

    Keep web process stateless
        What: don’t rely on local files or memory for critical data.
        Why: makes restarts safe and lets you scale horizontally later.
        Goal: reliability and easy scaling.

    Favor small, independent modules
        What: split features into separate files/modules.
        Why: changing one feature won’t break others.
        Goal: easier development and safer edits.

    Use async for I/O-heavy parts
        What: use async/await so one process can handle many requests while waiting on external APIs.
        Why: improves throughput on a single Railway dyno.
        Goal: handle more bot users without extra servers.

    Use environment variables for config
        What: keep tokens and settings in env vars (Railway already does this).
        Why: avoids leaking secrets in code and eases per-environment config.
        Goal: security and simple configuration.

    In-process task queue (lightweight)
        What: schedule background jobs inside the same process (async tasks + semaphore).
        Why: lets you offload long work without setting up Redis/Celery.
        Goal: responsiveness without extra infra.

    Minimize dependencies
        What: keep libraries small and few.
        Why: faster startup, fewer security bugs, easier maintenance.
        Goal: speed and simplicity.

Core components

    Web layer (FastAPI)
        What: receives Slack events and routes them to your code.
        Why: async + validation, low overhead.
        Goal: reliable, fast HTTP entrypoint.

    Dispatcher / Router
        What: central place mapping incoming events/commands to the right handler.
        Why: avoids big if/else blocks; new features register themselves.
        Goal: organized request handling and simple extensions.

    Handlers / Plugins
        What: each feature is a small module with register() and handle() functions.
        Why: encapsulates feature logic, easy to add/remove.
        Goal: modular, testable features.

    Services / Integrations
        What: small wrapper classes for external APIs (Slack, OpenAI, DeviantArt).
        Why: centralize retries, auth, and error handling.
        Goal: consistent external calls and easier testing.

    Storage (file_store / JSON)
        What: tiny JSON files or in-memory maps for small state (recent chat history, tokens).
        Why: avoids a DB for small projects on free plan.
        Goal: simple persistence without extra services.

    Caching (in-memory LRU / TTL)
        What: temporarily store frequently-requested data in memory.
        Why: fewer external calls, lower latency and cost.
        Goal: efficiency and speed.

    Rate limiting & circuit-breaker
        What: limit requests per user/service and pause calls if a service fails repeatedly.
        Why: prevents hitting API caps and reduces failures when third-party services are down.
        Goal: stability and graceful degradation.

    Background tasks / in-process queue
        What: run longer jobs asynchronously (file downloads, OpenAI calls) without blocking HTTP responses.
        Why: Slack demands quick ACKs; long tasks should run separately.
        Goal: responsiveness and non-blocking behavior.

    Concurrency controls (Semaphore)
        What: cap simultaneous background/API calls.
        Why: prevent exhausting memory/threads or triggering throttles.
        Goal: predictable load and safety on a single dyno.

Observability & operations

    Logging & structured logs
        What: consistent, searchable logs (JSON or clear format).
        Why: easier debugging and understanding failures.
        Goal: faster troubleshooting.

    Health / readiness endpoints
        What: /health or /ready HTTP routes that return app status.
        Why: Railway and you can check if the app is running.
        Goal: quick detection of broken deploys.

    CI (lint, tests)
        What: automated checks run on commits/PRs.
        Why: catch regressions and enforce code quality before deploy.
        Goal: safer changes and fewer bugs.

Design & patterns

    Dependency injection (pass services into handlers)
        What: give handlers service objects instead of global singletons.
        Why: easier to unit-test and swap implementations.
        Goal: maintainable testable code.

    Plugin registry (declarative registration)
        What: handlers register hooks instead of manual wiring.
        Why: onboarding a new feature is a simple file addition.
        Goal: extensibility and clarity.

    Schema validation (pydantic)
        What: validate incoming Slack payloads and config shapes.
        Why: catch malformed data early.
        Goal: safer and clearer code paths.

    Message formatting utilities
        What: small helpers to build Slack blocks/attachments.
        Why: consistent style and fewer formatting bugs.
        Goal: reliable message construction.

Scaling choices (lightweight-first)

    Keep web process stateless
        Repeat: makes swap to Redis/DB later trivial.

    Use in-memory caches and file-based state now
        What: cheap and simple for a single dyno.
        Why: fits Railway free limits.
        Goal: minimal infra, easy later migration.

    Replace file_store with Redis/Postgres later if needed
        What: same interface, new backend.
        Why: you keep code while upgrading infra.
        Goal: smooth growth path.

Security & reliability

    Verify Slack signatures
        What: confirm requests are from Slack.
        Why: prevents forged requests.
        Goal: account safety.

    Handle API errors and 429s
        What: catch rate limits and retry after waiting.
        Why: prevents choking the bot and avoids permanent failures.
        Goal: resilient external calls.

Migration & safety

    Port features incrementally
        What: move handlers one-by-one to the new architecture.
        Why: reduces risk and makes debugging easier.
        Goal: safer rebuild.

Practical short checklist (what to implement first)

    FastAPI app with Slack signature verification and /slack/events endpoint.
    Simple dispatcher that loads handlers from handlers/ folder.
    Slack service (post message) and OpenAI service (chat completion).
    File_store for small convo state and a memory cache for frequent items.
    One AI chat handler implementing convo storage + OpenAI calls.
    Health endpoint, structured logs, and basic rate limiting.
    Deploy to Railway and test in your workspace
