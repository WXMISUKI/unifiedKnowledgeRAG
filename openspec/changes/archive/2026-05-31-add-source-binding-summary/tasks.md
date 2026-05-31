## 1. Source Binding Summary

- [x] 1.1 Add response models and a provider source binding summary service.
- [x] 1.2 Expose `GET /api/provider/source-bindings` and advertise it in the provider manifest.
- [x] 1.3 Keep the summary read-only and based on existing catalog, manifest, preflight, and index readiness services.

## 2. Documentation And Specs

- [x] 2.1 Update README and lightweight roadmap with the source binding summary boundary.
- [x] 2.2 Update main OpenSpec specs for knowledge-provider and provider-roadmap.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for ready, drifted, not-ready, manifest, and read-only behavior.
- [x] 3.2 Run focused tests, full pytest, and strict OpenSpec validation.
- [x] 3.3 Archive the completed change and re-run strict spec validation.
