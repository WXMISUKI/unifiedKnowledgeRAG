## Why

The provider can already be started locally with `uvicorn app.main:app --reload --port 8020`, and MyPrivateAgent access readiness has been closed. The immediate goal is not server deployment or backend promotion; it is making the local day-1 run path obvious and verifiable.

Today `quickstart.md` only records the two startup commands. A local developer still needs a small, repeatable check that says whether the already-running service is usable: health, discovery, preflight, retrieval evidence, and answer behavior.

## What Changes

- Add a local usable run-loop report that validates an already-running local provider over HTTP.
- Check `/live`, `/ready`, `/health`, provider manifest, provider preflight, RAG retrieve, and RAG answer.
- Classify local usability as `go`, `review`, or `blocked`.
- Export JSON and Markdown evidence under `docs/local-run/`.
- Update quickstart and README local run instructions with the new run-loop command.
- Keep fixture/mock defaults; do not promote Qdrant, BGE-M3, pgvector, hybrid retrieval, GraphRAG, or deployment behavior.

## Capabilities

### New Capabilities

- `local-usable-run-loop`: Local-only run-loop smoke for deciding whether the provider is usable on the developer machine after startup.

### Modified Capabilities

- `provider-workstream-rebaseline`: The local run-loop is an explicit local usability check under the trigger-driven workflow, not a continuation of access-readiness phases.

## Impact

- Affected code: new local run-loop service, export script, and focused tests.
- Affected docs: quickstart, README local run instructions, generated local run-loop artifacts.
- Affected APIs: none.
- Dependencies: none beyond existing `httpx`.
- Systems: no runtime default changes, no model downloads, no Docker/Qdrant startup, no GraphRAG execution, no source binding creation.
