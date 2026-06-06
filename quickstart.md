# Start the local provider

```powershell
conda activate GRAPHRAG
uvicorn app.main:app --reload --port 8020
```

# Verify the local usable run-loop

Run this in another terminal after the provider is listening on port 8020:

```powershell
conda activate GRAPHRAG
python scripts/export_local_usable_run_loop.py --base-url http://127.0.0.1:8020
```

Default outputs:

```text
docs/local-run/local-usable-run-loop.json
docs/local-run/local-usable-run-loop.md
```

`Decision: go` means the local provider is usable for discovery, preflight,
retrieval evidence, and a cited answer. `review` means the local fixture query,
source id, or corpus needs review. `blocked` means the provider or contract path
must be fixed before local caller integration.
