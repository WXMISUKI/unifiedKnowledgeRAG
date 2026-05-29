## Context

The answer path has several provider-owned guardrails:

- prompt package construction
- prompt rendering
- output parsing
- output validation
- fail-closed answer envelope assembly

These currently live inside `DeterministicAnswerComposer`. That is fine for one composer, but it is the wrong shape before adding hosted or local composers. Model-specific composers should not reimplement provider-level citation safety and metadata conventions.

## Goals / Non-Goals

**Goals:**
- Introduce a shared finalizer that accepts query, evidence, candidate answer text, and base metadata.
- Preserve the current HTTP response and metadata for deterministic answers.
- Make invalid candidate output fail closed in the finalizer.
- Keep hosted/local composers unimplemented.

**Non-Goals:**
- Add LLM adapters.
- Change prompt wording, parser rules, validator rules, or answer endpoint shape.
- Add retry or repair behavior for invalid model output.

## Decisions

1. Finalizer accepts candidate answer text.

   Rationale: future model adapters naturally produce text. The finalizer then owns parsing and validation.

2. Finalizer owns prompt metadata.

   Rationale: prompt package/render metadata must remain consistent across all composers.

3. Invalid candidate output returns `insufficient_evidence`.

   Rationale: until a repair loop exists, unvalidated output must not be endorsed as answered.

## Risks / Trade-offs

- This is mostly refactoring plus tests -> It is valuable now because it prevents duplicated safety logic before model adapters arrive.
- Future structured tool-call composers may not produce text -> They can still adapt to the finalizer or a future finalizer variant once requirements are concrete.
