## 1. Specification

- [x] 1.1 Create proposal, design, delta specs, and tasks for approved local corpus source registration.
- [x] 1.2 Validate the OpenSpec change before implementation.

## 2. Implementation

- [x] 2.1 Add an approved local source registry service that validates handoff status, copies markdown into the provider source directory, writes registry JSON, and returns registered/blocked results.
- [x] 2.2 Add a CLI registration script with handoff, registry path, and source directory parameters.
- [x] 2.3 Include approved local sources in source catalog, source package metadata, source document manifests, and known-source checks.
- [x] 2.4 Allow fixture and LlamaIndex retrieval helpers to return stable evidence for approved local markdown sources.
- [x] 2.5 Add focused tests for ready registration, blocked handoffs, missing markdown, catalog visibility, manifest diagnostics, and retrieval/answer behavior.
- [x] 2.6 Update quickstart, README, roadmap, and progress tracker with the approved registration command and boundaries.

## 3. Verification And Archive

- [x] 3.1 Run focused approved local source registration tests.
- [x] 3.2 Run `openspec validate add-approved-local-corpus-source-registration --strict`.
- [x] 3.3 Register the real `company_profile_2025_trial` handoff and verify generated artifacts.
- [x] 3.4 Run focused local RAG retrieval/answer smoke for the registered source.
- [x] 3.5 Run `openspec validate --all --strict`.
- [x] 3.6 Archive the OpenSpec change after specs are synchronized.
