## 1. Probe API Contract

- [x] 1.1 Add a side-effect-free `/live` endpoint.
- [x] 1.2 Add a `/ready` endpoint that preserves the existing readiness response contract.
- [x] 1.3 Advertise `live` and `ready` endpoint paths from the provider manifest.

## 2. Deployment And Documentation

- [x] 2.1 Update Docker Compose healthcheck to use `/ready`.
- [x] 2.2 Update README, lightweight roadmap, and main OpenSpec specs.

## 3. Verification And Archive

- [x] 3.1 Add focused tests for liveness side effects, readiness compatibility, manifest discovery, and Compose probe path.
- [x] 3.2 Run focused tests, full pytest, and strict OpenSpec validation.
- [x] 3.3 Archive the completed change and re-run strict spec validation.
