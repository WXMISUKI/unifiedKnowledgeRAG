## 1. Readiness HTTP Contract

- [x] 1.1 Return HTTP 503 from `/ready` when provider readiness is degraded.
- [x] 1.2 Preserve `/ready` response body and keep `/health` HTTP status compatible.

## 2. Documentation And Specs

- [x] 2.1 Update README and lightweight roadmap with readiness HTTP status semantics.
- [x] 2.2 Update main OpenSpec specs for knowledge-provider and provider-roadmap.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for ready HTTP 200, degraded ready HTTP 503, and degraded health HTTP 200.
- [x] 3.2 Run focused tests, full pytest, and strict OpenSpec validation.
- [x] 3.3 Archive the completed change and re-run strict spec validation.
