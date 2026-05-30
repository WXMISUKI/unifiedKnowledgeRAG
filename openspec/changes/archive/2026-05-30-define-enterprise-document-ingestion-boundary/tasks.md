## 1. Specification

- [x] 1.1 Validate the enterprise ingestion boundary OpenSpec change.

## 2. Implementation

- [x] 2.1 Add ingestion preflight contract models.
- [x] 2.2 Implement source ingestion preflight service with markdown-only diagnostics.
- [x] 2.3 Expose `GET /api/ingestion/sources/{source_id}/preflight`.
- [x] 2.4 Update README and roadmap with the Phase 2 ingestion boundary.

## 3. Verification

- [x] 3.1 Add tests for ready markdown, missing file, unsupported format, unknown source, and side-effect-free behavior.
- [x] 3.2 Run focused tests, full tests, and strict OpenSpec validation.
