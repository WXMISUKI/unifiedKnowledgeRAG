## 1. Contract And Manifest

- [x] 1.1 Add provider integration manifest response models.
- [x] 1.2 Add a provider manifest service with stable identity, contract version, endpoint paths, evidence paths, and supported capability ids.
- [x] 1.3 Expose `GET /api/provider/manifest` and wire it into the FastAPI app.

## 2. Tests And Smoke

- [x] 2.1 Add focused contract tests for manifest identity, endpoints, capability ids, and side-effect-free shape.
- [x] 2.2 Extend provider contract smoke to include the manifest check.

## 3. Docs And Validation

- [x] 3.1 Document the integration manifest in README.
- [x] 3.2 Run focused and full pytest validation.
- [x] 3.3 Run OpenSpec strict validation and archive the change.
