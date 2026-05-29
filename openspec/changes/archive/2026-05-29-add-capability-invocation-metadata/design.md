## Context

Capability discovery currently exposes stable ids and status, but the caller must already know which HTTP method and path to use. That is enough for humans reading README, but not ideal for an agent control plane that wants to discover and invoke provider capabilities dynamically.

This change adds the smallest useful invocation descriptor while leaving richer registry design for later.

## Goals / Non-Goals

**Goals:**
- Add optional HTTP invocation metadata to each capability entry.
- Keep existing response shape backward compatible by preserving all existing fields.
- Make `knowledge.rag.retrieve` and `knowledge.rag.answer` directly discoverable with method/path.
- Mark planned graph query with its contract endpoint even though runtime execution still returns the existing not-implemented error.

**Non-Goals:**
- Add JSON schema references, OpenAPI links, auth policy, tenant policy, rate limits, or examples.
- Add a new capability registry persistence layer.
- Change any capability endpoint behavior.

## Decisions

1. Use a nested `invocation` object.

   Rationale: method/path belong together and can be extended later with protocol, schema refs, or streaming mode without flattening too many fields onto `Capability`.

   Alternative considered: add top-level `method` and `path`. Rejected because it is less extensible and makes non-HTTP capabilities awkward later.

2. Keep `invocation` optional.

   Rationale: future capability entries may be non-HTTP or intentionally non-invokable. Optional metadata preserves compatibility and flexibility.

## Risks / Trade-offs

- Callers may treat `planned` graph capability as executable -> Status remains `planned`, while invocation only identifies the contract endpoint.
- Richer registry needs will arrive later -> This slice intentionally stops at method/path because that unlocks immediate dynamic invocation without over-designing.
