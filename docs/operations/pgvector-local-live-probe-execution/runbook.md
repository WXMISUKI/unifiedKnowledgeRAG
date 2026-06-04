# Phase 12f PGVector Local Live Probe Execution Runbook

Use this runbook when you want to rerun the Phase 12d live probe locally after the Phase 12e environment package is in place.

## 1. Review The Current State

Start here:

- [phase12f-pgvector-local-live-probe-execution-readiness.md](phase12f-pgvector-local-live-probe-execution-readiness.md)
- `docs/operations/pgvector-local-live-probe-execution/phase12f-pgvector-local-live-probe-execution-readiness.json`
- `docs/operations/pgvector-local-probe-environment/phase12e-pgvector-local-probe-environment-readiness.json`
- `docs/operations/pgvector-live-probe-readiness/phase12d-pgvector-live-probe-readiness.json`

Confirm the current execution boundary:

- the Phase 12e local environment package is ready
- the Phase 12d live probe is still the evidence source that will be refreshed
- the local probe rerun path stays optional and read-only from the provider perspective

## 2. Prepare The Local Rerun

Use the existing Phase 12e environment package as the only local setup input:

- `requirements-pgvector.txt`
- `docker-compose.pgvector.example.yml`
- `docker/pgvector/init.sql`
- `.env.example`

Then rerun the live probe evidence:

```powershell
python scripts/export_phase12d_pgvector_live_probe_readiness.py
```

## 3. Refresh Local Evidence

After the rerun completes, refresh the surrounding evidence chain:

```powershell
python scripts/export_phase12f_pgvector_local_live_probe_execution_readiness.py
python scripts/export_provider_handoff_bundle.py
python scripts/export_provider_handoff_refresh.py
```

## 4. Recheck The Result

Reopen the generated evidence and verify:

- `phase12f-pgvector-local-live-probe-execution-readiness.json`
- `phase12d-pgvector-live-probe-readiness.json`
- `provider-handoff-bundle.json`
- `provider-handoff-refresh.json`

You want to see the execution state move from `ready_for_local_live_probe_rerun` toward a refreshed live-probe result.

## 5. Stop At The Boundary

Stop here if the next step would require:

- promoting pgvector to the runtime default
- changing GraphRAG execution, parser defaults, or answer policy
- making the provider own PostgreSQL governance or migration policy

Those are separate evidence-backed slices, not this runbook.

## 6. Keep It Current

When the rerun path changes, rerun:

```powershell
python scripts/export_provider_handoff_refresh.py
```

This runbook is current only when the evidence chain is current.
