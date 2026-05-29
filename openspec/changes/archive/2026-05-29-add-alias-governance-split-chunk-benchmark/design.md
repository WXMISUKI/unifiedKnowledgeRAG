# Design: Add Alias Governance And Split-Chunk Benchmark

## Context

`alias-aware-identifier-gate-v1` currently normalizes fixture-local aliases in code. That is acceptable for a local candidate, but production alias behavior needs explicit ownership, approval status, versioning, and risk notes. Separately, strict identifier gating requires every query identifier to appear in the same evidence chunk. This can be too strict when a procedure mentions a policy code in one paragraph and a form code in a nearby paragraph.

## Alias Governance Candidate

Use a local JSON catalog for evaluation:

- stable alias id;
- canonical identifier;
- pattern;
- owner;
- status;
- version;
- risk level;
- notes.

The evaluation should export catalog summary metrics and call out entries that are not approved.

## Split-Chunk Benchmark

Add a local fixture source where:

- `RFD-2026-003` appears in one paragraph;
- `AF-REFUND-02` appears in a nearby paragraph;
- the query asks for both identifiers.

Expected result for the strict gate is a documented miss. This is useful evidence because it tells us the next production direction may need parent/section context, multi-vector chunk aggregation, or reranking/evidence grading rather than only stricter gating.

## Boundary

This change produces local evidence only. It does not promote aliases, split-chunk aggregation, or runtime gating.
