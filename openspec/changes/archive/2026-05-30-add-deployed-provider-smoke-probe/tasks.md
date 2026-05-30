## 1. Probe Implementation

- [x] 1.1 Add a deployed provider smoke service that probes health, manifest, preflight, and handoff over HTTP.
- [x] 1.2 Add a CLI exporter with base URL, timeout, and optional provider API key support.

## 2. Evidence And Documentation

- [x] 2.1 Export JSON and Markdown smoke evidence without serializing secret values.
- [x] 2.2 Document the deployed smoke command in README and the lightweight provider roadmap.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for success, auth header propagation, fail-closed behavior, and export artifacts.
- [x] 3.2 Run focused tests, full pytest, and strict OpenSpec validation.
- [x] 3.3 Archive the completed change and re-run strict spec validation.
