## Why

The provider preflight endpoint now reports whether the default integration contract is bindable, but MyPrivateAgent also needs to ask whether a specific required contract version and capability set are supported before enabling a provider. Adding explicit requirement inputs turns preflight from a static readiness check into a compatibility gate while preserving the existing default behavior.

## What Changes

- Extend `GET /api/provider/preflight` with optional query parameters:
  - `required_contract_version`
  - repeated `required_capability_ids`
- Include requested requirements in the preflight response.
- Add a contract-version compatibility check.
- Make capability and schema-reference checks use the caller's requested capability ids when supplied.
- Keep default preflight behavior compatible when no query parameters are supplied.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `knowledge-provider`: extend provider preflight to support caller-supplied binding requirements.

## Impact

- Affected code: provider preflight models, service, router, focused tests, README, OpenSpec spec.
- API: extends existing `GET /api/provider/preflight` query contract without changing existing default response semantics.
- Dependencies: no new dependency, hosted model, vector database, queue, graph runtime, or MyPrivateAgent-side code.
