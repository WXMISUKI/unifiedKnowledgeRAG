## 1. Shared Builders

- [x] 1.1 Extract reusable health response construction from the health router.
- [x] 1.2 Extract reusable capability response construction from the capabilities router.

## 2. Preflight Endpoint

- [x] 2.1 Add provider preflight response models.
- [x] 2.2 Add a provider preflight service that checks manifest, health readiness, required capabilities, and schema refs.
- [x] 2.3 Expose `GET /api/provider/preflight` through the provider router.

## 3. Tests And Docs

- [x] 3.1 Add focused contract tests for default bindable, degraded readiness, planned graph details, and side-effect-free behavior.
- [x] 3.2 Extend provider contract smoke to include preflight.
- [x] 3.3 Document the provider preflight endpoint in README.

## 4. Validation

- [x] 4.1 Run focused and full pytest validation.
- [x] 4.2 Run OpenSpec strict validation and archive the change.
