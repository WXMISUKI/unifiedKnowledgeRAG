# Phase 12e PGVector Local Probe Environment Runbook

Use this runbook when you want to move from a blocked `phase12d` live probe to a reproducible local pgvector environment without changing runtime defaults.

## 1. Review The Current State

Start here:

- [phase12e-pgvector-local-probe-environment-readiness.md](phase12e-pgvector-local-probe-environment-readiness.md)
- `docs/operations/pgvector-local-probe-environment/phase12e-pgvector-local-probe-environment-readiness.json`
- `docs/operations/pgvector-live-probe-readiness/phase12d-pgvector-live-probe-readiness.json`

Confirm the current blockers:

- `PGVECTOR_DATABASE_URL` is not configured for the live probe
- the optional `psycopg` dependency is not installed in the base environment
- the local compose profile is not running unless you start it manually

## 2. Pick The Local Environment Mode

Choose the setup that matches your machine:

- Optional local dependency only
- Optional local compose profile
- Local compose profile plus exported environment variables

Use [config-reference.md](config-reference.md) to map the mode to concrete settings.

## 3. Apply The Environment Package

Update the environment and mounts that match the target mode:

- install `requirements-pgvector.txt` in a local-only environment
- start `docker-compose.pgvector.example.yml` with the `pgvector` profile
- let `docker/pgvector/init.sql` create the isolated schema, table, and index
- set `PGVECTOR_DATABASE_URL` to the local compose endpoint if you want to run the probe

Do not change runtime defaults unless the local probe target explicitly requires it.

## 4. Refresh Evidence

After changing configuration or mounted state, rerun:

```powershell
python scripts/export_phase12e_pgvector_local_probe_environment_readiness.py
python scripts/export_phase12d_pgvector_live_probe_readiness.py
python scripts/export_provider_handoff_bundle.py
python scripts/export_provider_handoff_refresh.py
```

Treat the refreshed outputs as the current source of truth.

## 5. Recheck The Result

Reopen the generated evidence and verify:

- `phase12e-pgvector-local-probe-environment-readiness.json`
- `phase12d-pgvector-live-probe-readiness.json`
- `provider-handoff-bundle.json`
- `provider-handoff-refresh.json`

You want to see whether the local environment package is ready, and whether the live probe has moved from `blocked` to `review` or `ready`.

## 6. Stop At The Boundary

Stop here if the remaining work would require:

- promoting pgvector to the runtime default
- making the provider own PostgreSQL governance or migration policy
- changing GraphRAG execution, parser defaults, or answer policy

Those are separate evidence-backed slices, not this runbook.

## 7. Keep It Current

When the local probe environment changes, rerun:

```powershell
python scripts/export_provider_handoff_refresh.py
```

This runbook is current only when the evidence chain is current.
