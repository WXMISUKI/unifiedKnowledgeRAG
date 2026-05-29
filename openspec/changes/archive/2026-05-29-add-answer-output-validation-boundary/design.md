## Context

Prompt packaging and rendering now define what evidence and citations a composer may use. The next missing boundary is validating the answer output before it is returned. Deterministic composition is safe today, but hosted or local LLM composers will need the same citation validation to prevent unsupported references from reaching callers.

## Goals / Non-Goals

**Goals:**
- Add a small provider-owned validator for cited answer outputs.
- Confirm answered results include citations and every citation is allowed by the prompt package.
- Attach compact validation metadata to answered results.
- Preserve insufficient-evidence behavior and existing deterministic output.

**Non-Goals:**
- Implement LLM output parsing.
- Validate factual correctness beyond citation membership.
- Add model-specific safety classifiers or rerankers.
- Change response shape outside existing metadata.

## Decisions

1. Validate citations against prompt-package allowed citations.

   Rationale: this is the core invariant the provider can enforce without a model-specific parser or semantic grader.

2. Treat invalid citations as insufficient evidence.

   Rationale: if the provider cannot endorse the answer's citations, it should fail closed rather than return an answer that may be unsupported.

3. Keep validation metadata compact.

   Rationale: callers need auditability without receiving internal validation implementation details.

## Risks / Trade-offs

- Citation membership does not prove the answer is factually correct -> This is a first guardrail; evidence grading and LLM evaluation remain separate future changes.
- Deterministic composer currently always passes -> Tests include the validator service directly so the failure path is covered before LLM adapters exist.
