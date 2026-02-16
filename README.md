# Atomic Agents

Minimal developer README with run and test instructions.

Prereqs
- Python 3.10+ (async/await features used)
- Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Environment
- Copy `.env.example` to `.env` and set `API_KEY`.

Run the interactive CLI

```bash
python -m src.main
# or use the provided Windows helpers: start-agent.bat / start-agent.ps1
```

Run the mycelium autonomous mat (example)

```py
from mycelium.constitution import RootSystem
from mycelium.execution_mat import ExecutionMycelium
import asyncio

root = RootSystem()
mat = ExecutionMycelium(root)
asyncio.run(mat.run_autonomous_cycles(interval_minutes=30))
```

Tests

```bash
pytest -q
```

Key files
- `src/core/agent.py` — agent lifecycle and safety checks
- `src/models/cerebras_client.py` — async model client + env vars
- `src/mycelium/constitution.py` and `src/mycelium/execution_mat.py` — governance and orchestration
