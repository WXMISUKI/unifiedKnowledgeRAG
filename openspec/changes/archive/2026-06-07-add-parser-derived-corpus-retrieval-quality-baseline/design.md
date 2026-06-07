## Context

The provider now supports a complete local path from normalized external parser artifacts to an approved local source ingestion loop. The next question is quality: whether the parser-derived company-profile corpus can answer practical business questions with stable citations and fail closed for unsupported questions.

The existing benchmark harness is broader and already contains candidate backend evidence. This slice stays smaller: a local-run quality baseline for one parser-derived corpus, using a compact query fixture and the current provider HTTP contracts.

## Goals / Non-Goals

**Goals:**
- Evaluate a small parser-derived company-profile query set with answerable and expected-empty cases.
- Record per-case retrieve/answer behavior, returned citations, expected citations, and invalid citations.
- Export quality metrics and a `go` / `review` / `blocked` decision.
- Give a clear next action: continue to Stage 4 candidate backend review only if this local quality baseline is acceptable.

**Non-Goals:**
- No Qdrant/pgvector/BGE-M3 promotion or default backend switch.
- No reranker, hybrid search, query rewrite, or chunking strategy promotion.
- No parser/OCR execution, MyPrivateAgent orchestration, source binding, `/api/chat` mutation, or GraphRAG execution.

## Decisions

- Use FastAPI `TestClient` by default, matching existing local acceptance smoke. This avoids requiring a running server and keeps the baseline repeatable in the repo.
- Use a JSON fixture for query cases. This keeps business questions visible and lets future parser-derived documents add a small focused case set without changing code.
- Treat HTTP contract failure or missing source readiness as `blocked`; treat answerable misses, citation mismatches, or negative-control leaks as `review`. This avoids overstating readiness while keeping local quality iteration lightweight.
- Keep thresholds conservative and explicit: all answerable cases must hit expected citations, expected-empty cases must stay empty, and invalid citations must be zero for `go`.

## Risks / Trade-offs

- The current parser-derived fixture is small -> Mitigation: treat this as a baseline gate, not a production benchmark.
- Deterministic/fixture retrieval may pass small cases too easily -> Mitigation: record the retrieval backend and recommend Stage 4 candidate review only after baseline quality is visible.
- Business cases may need adjustment as real corpus text improves -> Mitigation: keep the fixture small and local so it can evolve with real documents.
