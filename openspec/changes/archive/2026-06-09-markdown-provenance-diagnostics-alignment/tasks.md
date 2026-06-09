## 1. Spec And Diagnostics Scope

- [x] 1.1 Finalize the OpenSpec proposal, design, and spec deltas for markdown provenance diagnostics alignment
- [x] 1.2 Define how page-oriented provenance expectations differ from markdown section/exact-term provenance

## 2. Diagnostics Implementation

- [x] 2.1 Update chunk-quality diagnostics so non-page markdown provenance does not trigger page-coverage review by default
- [x] 2.2 Refresh the local and aggregate golden-case evidence after diagnostics alignment

## 3. Verification

- [x] 3.1 Add or update focused tests for paged-vs-markdown provenance diagnostics behavior
- [x] 3.2 Run focused pytest and `openspec validate --all --strict`

## 4. Documentation And Closure

- [x] 4.1 Refresh roadmap/progress documentation with the aligned provenance outcome and next-step rule
- [x] 4.2 Archive the OpenSpec change after verification while keeping runtime defaults unchanged
