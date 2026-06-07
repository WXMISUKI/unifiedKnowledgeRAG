## Context

The provider already has:

- `scripts/export_local_rag_business_corpus_usability_check.py --include-live-http`

MyPrivateAgent already has:

- `scripts/export_local_knowledge_provider_corpus_trial.py`

This change does not duplicate either implementation. It only reads their JSON reports and decides whether the local integration loop is closed.

## Inputs

- Provider report:
  `docs/local-run/rag-business-corpus-usability/local-rag-business-corpus-usability-check.json`
- MyPrivateAgent report:
  `D:/AI/AIcode/MyPrivateAgent/docs/integration/local-knowledge-provider-corpus-trial/local-knowledge-provider-corpus-trial.json`

## Decision Rules

- `go`: both reports have `decision=go`, the provider report includes live HTTP, and both target the same source id.
- `review`: no required report is blocked, but at least one report is not `go` or live HTTP was not included.
- `blocked`: either report is missing, malformed, blocked, or source ids conflict.

## Boundary

The closure reads reports only. It does not call provider HTTP endpoints, run MyPrivateAgent code, mutate source catalog, create bindings, promote retrieval defaults, or write caller state.

## Verification

- Run provider live HTTP usability check.
- Run MyPrivateAgent caller-side corpus trial.
- Run closure export.
- Run focused tests and OpenSpec validation.
