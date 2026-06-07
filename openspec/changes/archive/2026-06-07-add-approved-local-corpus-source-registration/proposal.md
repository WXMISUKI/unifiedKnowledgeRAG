## Why

The local PDF-derived company profile corpus has already passed the local trial and caller handoff gates, but it still remains outside the provider's usable source catalog. The next lightweight step is to let an explicitly approved local markdown corpus become a provider-visible, retrievable source without introducing a heavy ingestion platform or caller-owned binding workflow.

## What Changes

- Add a local approved-source registration command that accepts a `ready_for_caller_review` local corpus handoff.
- Persist a small local approved source registry and copy the approved markdown into the provider source directory.
- Include approved local sources in provider source catalog, package metadata, source document manifest, and lightweight retrieval paths.
- Add focused tests and one real registration smoke for `company_profile_2025_trial`.
- Preserve runtime defaults and provider boundaries: no OCR startup, no raw PDF ingestion, no source-to-agent binding, no MyPrivateAgent orchestration, no Qdrant/BGE promotion, and no GraphRAG execution.

## Capabilities

### New Capabilities

- `approved-local-corpus-source-registration`: Covers explicit local approval, registry persistence, source materialization, and registration status for a trial/handoff-approved markdown corpus.

### Modified Capabilities

- `knowledge-provider`: Catalog and known-source checks include approved local corpus sources after registration.
- `document-rag`: Source document manifest and retrieve/answer paths can use approved local markdown sources with stable citation fallback.
- `local-corpus-caller-handoff`: A `ready_for_caller_review` handoff can feed a separate explicit registration step, while non-ready handoffs cannot be promoted.

## Impact

- Affected code: source catalog, source package metadata, source document manifest, fixture/LlamaIndex retrieval helpers, a new registration service, a new CLI script, and focused tests.
- Affected local files: a generated approved source registry under `app/data/local_sources/` and approved markdown under `app/data/sources/`.
- APIs remain shape-compatible; existing fixture sources and runtime defaults are preserved.
