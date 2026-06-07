## Why

Parser-derived documents can now enter the local ingestion loop, but the next useful question is whether that corpus can answer local business questions with stable citations and safe negative-control behavior. This change adds a lightweight retrieval quality baseline before considering vector backend promotion.

## What Changes

- Add a parser-derived corpus retrieval quality baseline for the current approved local company-profile source.
- Evaluate a small customer-like query set with answerable and expected-empty cases.
- Export hit rate, citation match rate, empty handling rate, invalid citation count, per-case evidence, and a `go` / `review` / `blocked` decision.
- Add a CLI exporter under `docs/local-run/parser-derived-corpus-retrieval-quality-baseline/`.
- Update roadmap/progress notes so Stage 3b is closed and the next gate becomes parser-derived retrieval quality, not GraphRAG or runtime vector promotion.

## Capabilities

### New Capabilities
- `parser-derived-corpus-retrieval-quality-baseline`: Defines the local quality baseline for parser-derived RAG corpus retrieval and answer evidence.

### Modified Capabilities
- `retrieval-benchmark-harness`: Clarifies that parser-derived corpus quality baselines are lightweight local evidence and do not imply backend promotion.

## Impact

- Affected code: new local service and CLI exporter.
- Affected data: small parser-derived company-profile quality case fixture.
- Affected tests: focused quality decision tests for go, review, and blocked states.
- No new parser, OCR, vector database, embedding model, reranker, MyPrivateAgent, or GraphRAG dependency.
