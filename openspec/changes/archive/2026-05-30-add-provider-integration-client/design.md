## Overview

Add a local `provider_integration_client` service that accepts a TestClient-like HTTP client and executes the provider binding sequence:

1. `GET /api/provider/manifest`
2. `GET /api/provider/preflight` with optional required contract/capability requirements
3. `GET /api/capabilities`

The result is a serializable report suitable for MyPrivateAgent registration checks, local smoke validation, and documentation.

## Decisions

- Use a client protocol based on `.get(path, params=...)` and `.json()` so FastAPI `TestClient`, httpx-like clients, or a thin MyPrivateAgent adapter can reuse the same logic.
- Keep the probe read-only. Capability `example_request` payloads are collected but not executed.
- Fail closed when HTTP status is non-200, JSON is malformed, preflight is not bindable, or required invocation examples are missing.
- Avoid Pydantic model dependencies for the probe report; dataclasses keep the helper lightweight and easy to copy into MyPrivateAgent later.

## Non-Goals

- No remote URL client factory in this slice.
- No authentication, TLS, retry, timeout, or service discovery policy.
- No SDK packaging decision.
- No execution of `/api/rag/retrieve`, `/api/rag/answer`, ingestion, or graph query endpoints.

## Compatibility

The change is additive and service-only. Existing HTTP contracts remain unchanged.
