## Context

The provider has a strong local lifecycle surface, but create-job still couples request handling to index building. A real production queue needs choices about workers, leases, persistence, concurrency, observability, embeddings, and vector stores. Those choices should be discussed before adopting external infrastructure.

This change introduces only the state-machine boundary: a job can be queued, then explicitly run by a local endpoint.

## Goals / Non-Goals

**Goals:**

- Support queued job creation without immediate indexing.
- Add explicit local run-next processing.
- Preserve synchronous create behavior by default.
- Reuse durable `jobs.jsonl` latest-state semantics.
- Keep cancellation and stale recovery compatible with queued/running states.

**Non-Goals:**

- No background thread, scheduler, external queue, lock service, worker pool, or distributed lease.
- No embedding model, vector database, chunking, or reranker decision.
- No tenant/auth policy.
- No UI.

## Decisions

1. Use `run_mode` on create instead of replacing existing behavior.

   Existing tests and contract users keep synchronous behavior. Callers opt into queued behavior with `run_mode="queued"`.

2. Model runner as explicit endpoint.

   `POST /api/ingestion/jobs/queue/run-next` is deterministic and easy to verify. A future background worker can call the same service function.

3. Reuse terminal append semantics.

   The runner appends `running` and then terminal `completed` or `failed` records for the selected queued job.

4. Select oldest queued job first.

   FIFO is predictable and enough for local execution.

## Risks / Trade-offs

- Manual runner endpoint is not production automation -> intentional for this slice.
- No lease means multiple concurrent runner calls are not safe -> out of scope until true worker design.
- Queued jobs may remain queued forever unless run -> visible in list/detail and can be canceled.

## Migration Plan

1. Extend request/response models.
2. Add queued create path.
3. Add run-next service and route.
4. Add tests and docs.
5. Validate and archive.
