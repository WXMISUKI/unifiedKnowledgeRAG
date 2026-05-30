# Change: Add RAG request filter context

## Why

`RagRetrieveRequest` already accepts a `filters` object, and the Qdrant adapter already supports tenant, document id, and ACL payload filters at the vector-store boundary. However, the HTTP RAG endpoints do not yet normalize or pass request filters into the retrieval backend. This creates a gap for enterprise usage where tenant isolation, ACL scoping, role-aware retrieval, and audit context must be explicit.

This change makes request filter context a first-class provider-owned boundary before deeper production authorization work begins.

## What Changes

- Add a compact request filter context helper that normalizes supported filter keys.
- Pass normalized filter context through document retriever backends.
- Apply supported filters to Qdrant text retrieval.
- Include filter context metadata in retrieval and answer responses for diagnostics and audit.
- Preserve current fixture and LlamaIndex behavior while reporting that filters were accepted but not backend-enforced there.

## Non-Goals

- No authentication or authorization policy engine.
- No ACL enforcement for fixture or LlamaIndex backends.
- No new filter schema beyond the supported keys in this change.
- No changes to source catalog ownership or graph query behavior.
