# Phase 12e PGVector Local Probe Environment Config Reference

This page maps the local pgvector probe environment to the files and environment variables that make it reproducible. It is a reference, not a policy document.

## Canonical Sources

- `requirements-pgvector.txt`
- `docker-compose.pgvector.example.yml`
- `docker/pgvector/init.sql`
- `.env.example`
- `docs/operations/pgvector-local-probe-environment/phase12e-pgvector-local-probe-environment-readiness.json`

## Environment Variables

| Variable | Suggested Value | Purpose |
|---|---|---|
| `PGVECTOR_DATABASE_URL` | `postgresql://unified_knowledge_rag:unified_knowledge_rag@localhost:5433/unifiedKnowledgeRAG` | Local probe connection string |
| `PGVECTOR_SCHEMA` | `unified_knowledge_rag` | Isolated schema for the probe environment |
| `PGVECTOR_TABLE` | `knowledge_chunks` | Probe table name |
| `PGVECTOR_INDEX_NAME` | `knowledge_chunks_embedding_idx` | Probe index name |
| `PGVECTOR_VECTOR_SIZE` | `1024` | Probe vector width |
| `PGVECTOR_PROBE_TIMEOUT_SECONDS` | `5` | Local probe timeout |

## Optional Local Dependency

- `psycopg[binary]>=3.2,<4`

Install it only in a local environment that will actually run the live probe.

## Local Compose Profile

Use the `pgvector` profile from `docker-compose.pgvector.example.yml` when you want a disposable local database for probe work.

## Init SQL

`docker/pgvector/init.sql` creates:

- the `vector` extension
- the isolated `unified_knowledge_rag` schema
- the `knowledge_chunks` table
- the `knowledge_chunks_embedding_idx` index

## Evidence Commands

Use these commands to refresh evidence after config changes:

```powershell
python scripts/export_phase12e_pgvector_local_probe_environment_readiness.py
python scripts/export_phase12d_pgvector_live_probe_readiness.py
python scripts/export_provider_handoff_refresh.py
```

## Boundary Notes

- This reference does not promote pgvector to runtime default.
- This reference does not own PostgreSQL governance, audit policy, or migration policy.
- This reference should be updated whenever the local probe environment files change.
