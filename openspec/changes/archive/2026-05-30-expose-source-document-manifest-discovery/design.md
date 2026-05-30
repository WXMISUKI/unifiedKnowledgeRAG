## Context

`unifiedKnowledgeRAG` uses provider manifest, `/api/capabilities`, preflight, smoke reports, and integration probes as the stable binding surface for MyPrivateAgent and other callers. The new source document manifest endpoint is intentionally read-only and diagnostic, but it should still be discoverable in the same provider-owned binding surface as retrieval and answer capabilities.

## Goals / Non-Goals

**Goals:**

- Make `GET /api/rag/sources/{source_id}/documents` discoverable without reading README or guessing paths.
- Keep preflight useful for read-only GET capabilities that do not have request body schemas.
- Keep provider smoke and integration probe evidence current after adding the diagnostic endpoint.

**Non-Goals:**

- Do not execute the source document manifest endpoint inside binding probes by default.
- Do not add authentication, registration, heartbeat, or caller policy behavior.
- Do not promote any retrieval backend, embedding model, reranker, or GraphRAG behavior.

## Decisions

- Add capability id `knowledge.rag.source_documents` with a GET invocation, path template, response schema ref, and example path parameters. This keeps the endpoint discoverable while clearly separating it from query-time retrieval.
- Add `rag_source_documents_template` to provider manifest endpoints. Manifest consumers can find the endpoint even if they do not inspect capabilities deeply.
- Update schema-reference preflight so GET capabilities can pass when they have a response schema and example request/path parameters but no request body schema. This reflects HTTP reality without weakening POST capability checks.
- Keep the new capability in default required capability ids. A caller that expects this provider contract can fail closed if the diagnostic surface disappears.

## Risks / Trade-offs

- Adding a capability id broadens the default binding surface. Mitigation: the capability is read-only and local to diagnostics; it does not require extra infrastructure.
- Path-template capabilities do not map cleanly to request body schemas. Mitigation: require response schema refs and example path parameters for GET diagnostics.
- Integration probes remain metadata-only. Mitigation: contract tests cover the endpoint behavior separately, while probes avoid accidental runtime work.
