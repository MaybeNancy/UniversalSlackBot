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

################################
Code File Tree (Temporal):

    .github/
        workflows/
            ci.yml
    .gitignore
    Procfile
    README.md
    requirements.txt
    pyproject.toml (optional)
    runtime.txt (optional)
    app.py # top-level FastAPI app instance for Gunicorn: app
    src/
        main.py # optional CLI/start helper or alternative app export
        config.py # loads env vars, constants
        server.py # create_app() factory used by app.py
        routes/
            slack.py # Slack HTTP endpoints: /slack/events, /slack/interact, /health
        dispatcher.py # maps events/commands to handlers; plugin registry
        context.py # Context object passed to handlers (services, storage, logger)
        handlers/
            init.py
            ai_chat/
                init.py
                handler.py
                schema.py
            deviantart_search/
                init.py
                handler.py
                schema.py
            ping/
                handler.py
        services/
            init.py
            slack_service.py
            openai_service.py
            deviantart_service.py
            httpx_client.py
        storage/
            init.py
            storage_interface.py
            file_store.py
            memory_store.py
        tasks/
            background.py
            pruner.py
        utils/
            logging.py
            rate_limiter.py
            lock.py
            slack_format.py
        tests/
            test_file_store.py
            test_dispatcher.py
            test_ai_handler.py
    data/
        file_store/
            convos/
            cache/
            flags.json
            meta.json
    docs/
        architecture.md
        handler_guidelines.md

###########################
Code suggestions with new architecture in mind:
Project structure & entry

    Move logic into modules (routes, handlers, services, storage) instead of a single file.
        Why: separation of concerns; easier testing and incremental porting.
    Expose FastAPI app from top-level app.py that uses a create_app() from src/server.py.
        Why: simple deployment (gunicorn app:app) and clean startup hooks.

Request verification & routing

    Centralize Slack signature verification into a single middleware/utility used by all Slack endpoints.
        Why: avoid duplicated verification logic and ensure consistency.
    Add explicit URL verification (handle Slack "challenge") in your events route.
        Why: necessary for Slack Events registration.

Async-first design

    Replace blocking requests with an async HTTP client and make route handlers async.
        Why: lets a single Railway dyno handle many concurrent OpenAI/DA requests.
    Ensure long-running operations are offloaded to background tasks (ack Slack immediately).
        Why: prevents Slack timeouts and keeps responses snappy.

Dispatcher & handlers

    Implement a small dispatcher: routes events/commands to handler modules instead of large if/elif.
        Why: makes adding/removing commands simple and isolates behavior.
    Convert each current command (echo, /da, ai chat) into separate handler modules with a register() interface.
        Why: modularity and safer incremental migration.

Services layer

    Move Slack API calls (postMessage, delete) into a SlackService wrapper; do not call Slack API directly from handlers.
        Why: single place for auth, retries, rate-limit handling and easier testing.
    Encapsulate DeviantArt interactions in a DeviantArtService (token management, search/gallery/tag).
        Why: isolate token refresh logic and error handling.
    Add an OpenAIService for chat completions with prompt templates and convo assembly.
        Why: centralize rate limiting, cost controls, and prompt engineering.

Storage: file_store specifics

    Implement a file_store that provides get/set/delete/list with optional TTL and atomic writes.
        Why: safe, minimal persistence on single dyno.
    Store bounded conversation history per user (e.g., last 8–12 messages) and small caches (DA metadata).
        Why: reduces cost and keeps prompts compact.
    Use an in-memory LRU cache layer on top of file_store for hot keys to reduce IO.
        Why: improve latency and reduce disk writes.

Concurrency & safety

    Use an asyncio.Semaphore to limit concurrent external API calls (global and per-service caps).
        Why: avoid saturating CPU/conn limits or hitting third-party rate limits.
    Use per-namespace async locks when writing files to prevent race conditions.
        Why: avoid file corruption on concurrent writes.

Error handling & resilience

    Add retry/backoff for external API calls and treat 429s specially (respect Retry-After).
        Why: robustness and polite API usage.
    Implement simple circuit-breaker behavior for flaky services (trip after N failures, cool down).
        Why: avoid repeated expensive failures and degrade gracefully.

Message handling & UX

    Normalize and validate incoming Slack event payloads; ignore bot messages and messages without text/subtype.
        Why: prevent loops and unexpected errors.
    For image/video sending, build blocks with helper utilities and fall back gracefully if block types unsupported.
        Why: consistent message format and fewer failures.

Rate limiting & abuse control

    Implement per-user and per-command token bucket limiter (small quotas) to prevent abuse and cost blowups.
        Why: protect OpenAI spend and avoid hitting API limits.

Testing & local dev

    Add unit tests using memory_store; avoid file IO in unit tests except for integration tests.
        Why: fast, deterministic tests.
    Use ngrok/localtunnel for local Slack testing; keep environment-specific configs out of code.
        Why: test webhooks locally safely.

Observability

    Add structured logs with request correlation IDs; log key events (incoming event type, handler invoked, errors).
        Why: easier debugging on Railway where you have limited access.
    Add /health and /ready endpoints.
        Why: quick checks and platform probes.

Deployment & operations

    Keep secrets only in Railway env vars (you already do).
        Why: avoid secrets in repo.
    Start with one worker/process on Railway; tune concurrency (async) instead of spawning many processes to keep within free plan.
        Why: conserve memory and stay within limits.

Migration approach

    Port features incrementally:
        First: minimal slack endpoints + SlackService + dispatcher + ping handler.
        Next: file_store + AI chat handler (bounded convo store + OpenAIService).
        Then: DeviantArtService + /da handler, using file_store cache for DA results.
        Why: safe rollouts and easier bisecting.
    Keep the old bot running during migration and test each handler in a dev Slack workspace before switching production.
        Why: reduces downtime risk.

Security & housekeeping

    Don’t log raw secrets or full request bodies; redact tokens and PII in logs.
        Why: security and compliance.
    Rotate DA/OpenAI tokens if supported; add simple alerting if tokens fail repeatedly.
        Why: reliability.

Small code-quality notes (non-code)

    Replace global mutable variables (DA_token, rando, perm_bot_msg) with per-service or per-request state managed by services or file_store.
        Why: globals create hidden coupling and bugs.
    Remove commented-out dead code or move it into docs/ if you want to keep examples.
        Why: reduces confusion.

Priority checklist (minimum viable refactor steps)

    Create app skeleton (app.py, src/server.py, routes/slack.py).
    Add SlackService + signature verification and a simple /slack/events handler that delegates to dispatcher.
    Implement dispatcher and a simple ping handler to test flow.
    Build file_store (get/set/ttl) and memory_store for tests.
    Implement OpenAIService and basic ai_chat handler storing bounded convo history in file_store.
    Implement DeviantArtService and convert /da command to use it with caching.
    Add concurrency limits, retries, logging, health endpoint, and deploy.
