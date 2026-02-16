## Purpose
Help AI coding agents be productive in this repo by describing architecture, conventions, run/test workflows, integration points, and where to look for examples.

### Big picture (read these first)
- **Three layers**: lightweight CLI/content utilities (`src/main.py`, `src/content/*`), core agent runtime (`src/core/*`, `src/models/cerebras_client.py`), and the autonomous trading/mycelium system (`src/mycelium/*`).
- **Control & enforcement**: `mycelium/constitution.py` (RootSystem) enforces limits; `execution_mat.py` is the orchestrator for hypha nodes.
- **Model integration**: `models/cerebras_client.py` is the async client used by agents (`AIChatbot` in `src/core/agent.py`). It requires `API_KEY` and optionally `BASE_URL`, `MODEL`, `MAX_TOKENS`, `TEMPERATURE` env vars.

### Runtime & developer workflows
- Install deps: `pip install -r requirements.txt` (see `requirements.txt`).
- Environment: create a `.env` with `API_KEY=...` and optional `BASE_URL` / `MODEL` / `MAX_TOKENS` / `TEMPERATURE`.
- Run the interactive CLI: from repo root run `python -m src.main` (Windows alternatives provided as `start-*.bat` / `start-*.ps1`).
- Run mycelium autonomous mat: import and run `ExecutionMycelium` (see `src/mycelium/execution_mat.py`). The mat spawns hyphae and runs cycles asynchronously.
- Tests: run `pytest -q` (project uses `pytest-asyncio` for async tests).

### Important conventions & patterns (project-specific)
- Async-first design: most I/O and orchestration is `async`/`await`. Use `async with CerebrasClient()` and `asyncio.run(...)` for entry points.
- Dataclasses for domain messages/insights (`models.cerebras_client.Message`, `mycelium` node insights). Preserve dataclass shapes when changing message flow.
- Safety & gating: `core/safety.SystemSafety` is consulted on both inputs and outputs (see `src/core/agent.py`). If a change affects prompt construction, update safety checks.
- Constitution-first: any trade or capital movement must call `RootSystem.register_hypha`, `record_profit`, or `record_loss`. Hypha nodes expect the registry entries to exist and call back into `root`.
- Traces/logs: growth events append JSONL to `data/mycelium/growth_logs/YYYYMM.jsonl` (see `_log_growth_event`). Do not break this path if adding telemetry.

### Integration points and external dependencies
- Model endpoint: `models/cerebras_client.CerebrasClient` — uses `aiohttp` and `tenacity` for retries. Throwing or missing `API_KEY` prevents runs.
- Data engines and strategies: `finance/data_engine.py` and `finance/strategies/core_strategies.py` provide market data and signal generation used by hyphae.
- Persisted data: `data/products/` and `data/mycelium/` are written by CLI and mycelium respectively. Tests may rely on these paths.

### Quick examples (copy/paste friendly)
- Call the model (pattern):

  ```py
  async with CerebrasClient() as client:
      resp = await client.complete(messages)
      text = resp.content
  ```

- Hypha trade pattern (see `src/mycelium/nodes/crypto_hypha.py`): call `root.record_profit()` or `root.record_loss()` and update local P&L. Respect trade size limits (nodes cap trades e.g., `min(capital * 0.2, 50)`).

### Safety & secrets
- Never hardcode `API_KEY` in source. Use `.env` and the existing `CerebrasClient` env resolution.
- `SystemSafety` contains hard-coded regex policies; if you change policy names or actions, update `core/agent.py` handling which maps `allowed` -> agent state `SAFETY_BLOCKED`.

### When modifying or adding agents
- Follow existing agent lifecycle: set `state` on start/error, push messages into `conversation_history` (dataclass `ConversationMessage`), check safety before and after model calls, and persist meaningful events.
- Update `requirements.txt` when adding runtime deps.

### Files to inspect for examples
- `src/core/agent.py` — agent lifecycle and safety checks
- `src/models/cerebras_client.py` — async model client + env vars
- `src/mycelium/constitution.py` and `src/mycelium/execution_mat.py` — governance and orchestration
- `src/mycelium/nodes/` — examples of specialty nodes and trade/report patterns

If anything here is unclear or you want additional, targeted examples (tests, PR checklist, or a brief contributing section), tell me which area to expand.
