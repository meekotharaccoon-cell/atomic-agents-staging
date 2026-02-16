# Contributing

Small guidelines for code changes, tests, and PRs.

- Follow existing async-first patterns (`async` / `await`).
- When adding network calls, use `async with CerebrasClient()` or create new async clients.
- Update `requirements.txt` when adding runtime dependencies.
- If you change agent prompts or message shapes, update `src/core/agent.py` safety checks and `models/cerebras_client.Message` dataclass if needed.
- Tests: add pytest-compatible tests; use `pytest-asyncio` for async tests.
- Logging & telemetry: growth events are appended to `data/mycelium/growth_logs/YYYYMM.jsonl`. Preserve format when changing `_log_growth_event`.

Before opening a PR

- Run `pytest -q` and ensure no regressions.
- Include a brief description of the change and why it was necessary.
