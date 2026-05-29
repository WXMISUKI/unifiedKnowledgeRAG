## Context

The provider already owns prompt packaging, prompt rendering, and citation validation. The missing piece before real LLM adapters is output parsing: converting raw answer text into structured answer text plus citations. Deterministic output can use the same parser now, proving the boundary before hosted/local composers exist.

## Goals / Non-Goals

**Goals:**
- Add a dependency-free parser for bracketed citations such as `[refund_policy_2026#section-3]`.
- Preserve citation order while removing duplicates.
- Expose compact parser metadata in answered results.
- Ensure missing citations fail validation through the existing validator.

**Non-Goals:**
- Parse arbitrary markdown footnotes or provider-specific tool-call formats.
- Validate factual correctness.
- Implement LLM adapters or retry/repair prompts.

## Decisions

1. Parse bracketed citations.

   Rationale: the deterministic answer format and prompt policy already use bracketed citations, and this maps cleanly to common LLM answer instructions.

2. Preserve answer text unchanged.

   Rationale: the parser boundary should extract structure, not rewrite or sanitize answer content in this slice.

3. Attach parser metadata only for answered candidates.

   Rationale: insufficient-evidence results do not have endorsed generated output to parse.

## Risks / Trade-offs

- LLMs may emit malformed citations -> This parser will surface missing or invalid citations to the validator; repair loops remain future work.
- Bracket parsing is intentionally narrow -> That keeps the contract simple until a real model adapter proves additional formats are necessary.
