## 1. Specification

- [x] 1.1 Validate the provider API key guard OpenSpec change.

## 2. Implementation

- [x] 2.1 Add optional provider API key setting.
- [x] 2.2 Add FastAPI middleware for `/api/*` access guard.
- [x] 2.3 Update deployment readiness and documentation with redacted access-guard state.

## 3. Verification

- [x] 3.1 Add tests for default-open local behavior, missing token, bad token, bearer token, provider-key header, and public health.
- [x] 3.2 Run focused tests, full tests, and strict OpenSpec validation.
