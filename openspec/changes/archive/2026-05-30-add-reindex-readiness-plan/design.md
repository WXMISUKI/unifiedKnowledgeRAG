## Context

The provider already supports ingestion jobs, persisted source index status, job retention, stale-running recovery, and deployment readiness reporting. Reindexing remains an operator-triggered action. Before operators rebuild indexes, they need a compact read-only report that says what sources exist, whether source files are present, what index status is known, and which command should be used next.

## Goals / Non-Goals

**Goals:**
- Export a local, deterministic reindex readiness plan.
- Include per-source status and recommended actions.
- Include operational notes for backup/reindex review.
- Avoid any side effects.

**Non-Goals:**
- Do not create ingestion jobs.
- Do not delete or compact jobs.
- Do not rebuild indexes.
- Do not choose production queue or worker infrastructure.

## Decisions

1. Keep this as a CLI/export artifact rather than an API endpoint.
   - Rationale: reindex planning is an operator workflow, not caller retrieval behavior.

2. Use existing lifecycle truth sources.
   - Source catalog from `KNOWLEDGE_BASES`.
   - Index status from `get_index_status`.
   - Job history from `IndexLifecycleStore`.

3. Recommend actions but do not execute them.
   - Ready sources get `reindex_optional`.
   - Missing source files get `restore_source_file_before_reindex`.
   - Not indexed or failed sources get `run_ingestion_job`.

## Risks / Trade-offs

- Fixture backend always reports ready -> The report still notes that fixture does not require persisted indexes.
- Job history can be empty in fresh deployments -> Empty history is expected and should not block review by itself.
- Future production workers may add more states -> Use a versioned `reindex-readiness-v1` report with additive fields later.
