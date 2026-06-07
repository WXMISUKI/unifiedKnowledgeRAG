## Overview

The loop is intentionally a thin local orchestration layer over existing provider capabilities:

1. Run local document source onboarding.
2. Run ingestion preflight for the registered source.
3. Create an explicit ingestion job.
4. Read index status.
5. Run approved local corpus acceptance smoke.

The result is a single `go / review / blocked` report that tells the operator whether the source is usable for local RAG trials.

## Decision Semantics

- `go`: onboarding is `go`, preflight is `ready`, ingestion job completes, index status is `ready`, and acceptance smoke is `go`.
- `review`: no step is blocked, but a non-terminal step requires review, such as acceptance smoke review.
- `blocked`: a required step fails or a safety boundary is missing.

## Lightweight Boundary

The loop may create an explicit local ingestion job because that is the capability being verified. It SHALL NOT:

- parse raw PDFs as a supported provider format
- start OCR/Layout/VLM services
- call MyPrivateAgent
- create source-to-agent binding
- mutate `/api/chat`
- promote retrieval backend defaults
- call vector databases unless the current configured backend already does so through the existing ingestion job
- execute GraphRAG
- introduce a background worker or queue scheduler

## Implementation Notes

The service should accept dependency callables for onboarding, preflight, ingestion job, index status, and acceptance smoke so tests can cover state transitions without running heavy provider paths.

The CLI should default to the existing company profile trial values and write:

- `local-approved-source-ingestion-loop.json`
- `local-approved-source-ingestion-loop.md`

