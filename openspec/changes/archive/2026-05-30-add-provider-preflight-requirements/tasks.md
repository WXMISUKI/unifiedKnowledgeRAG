## 1. Contract

- [x] 1.1 Add requested requirement fields to the preflight response model.
- [x] 1.2 Add optional required contract version and capability id inputs to the preflight service.
- [x] 1.3 Wire preflight query parameters through the provider router.

## 2. Compatibility Checks

- [x] 2.1 Add exact contract-version compatibility check.
- [x] 2.2 Make required capability and schema-reference checks use caller-supplied capability ids when present.
- [x] 2.3 Preserve current default preflight behavior when no query parameters are supplied.

## 3. Tests And Docs

- [x] 3.1 Add focused tests for matching and mismatching contract versions.
- [x] 3.2 Add focused tests for matching and missing required capability ids.
- [x] 3.3 Document preflight requirement query parameters in README.

## 4. Validation

- [x] 4.1 Run focused and full pytest validation.
- [x] 4.2 Run OpenSpec strict validation and archive the change.
