# Design: Answer trace metadata

## Overview

`metadata.answer_trace` will be a compact provider-owned summary of the answer decision pipeline. It is intended for machine consumers, not for end-user display. The trace summarizes which stages ran, whether each stage passed, and the machine-readable reason for failure when applicable.

## Trace Shape

The trace will include:

- `trace_id`: deterministic local trace id for the response.
- `version`: trace contract version.
- `final_status`: the same value as `result.answer_status`.
- `stages`: ordered list of stage summaries.

Each stage summary will include:

- `name`
- `status`
- `reason`
- optional compact counters or identifiers such as `document_count`, `citation_count`, `backend`, `provider`, and `model`.

## Stage Semantics

For answered results:

1. `retrieval` summarizes backend and retrieved document count.
2. `evidence_gate` reports pass/fail and gate reason.
3. `composer` identifies the composer provider/model.
4. `output_parser` reports extracted citation count.
5. `output_validator` reports validation status and reason.
6. `final_decision` reports the final answer status.

For insufficient evidence before finalization, only stages that actually ran are included. For finalizer validation failure, parser and validator stages are included and `final_decision` reports insufficient evidence.

## Compatibility

Existing metadata keys remain unchanged. `answer_trace` is additive and should not require MyPrivateAgent to change its current answer parsing immediately.
