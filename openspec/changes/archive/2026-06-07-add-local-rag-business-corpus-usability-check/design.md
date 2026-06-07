## Context

Existing services already cover the pieces needed for local usability:

- `local_business_corpus_trial`: validates a markdown-derived business corpus fixture without registering a source.
- `approved_local_corpus_acceptance_smoke`: validates registered source behavior through in-process FastAPI calls.
- `approved_local_corpus_live_http_smoke`: validates the same behavior through live HTTP against an already running provider.

The next step should not create a heavier provider control plane. It should give a single answer to: "Can we use this local business corpus now?"

## Approach

Add `LocalRagBusinessCorpusUsabilityCheckService`.

The service runs:

1. Local corpus trial.
2. In-process approved corpus acceptance smoke.
3. Optional live HTTP smoke when explicitly requested.

It returns one compact report:

- `decision`: `go`, `review`, or `blocked`
- `reason_code`
- `source_id`
- `base_url`
- `checks`
- `summary`
- `recommended_actions`
- `non_goals`

Decision rules:

- `blocked`: any required check is blocked.
- `review`: no required check is blocked, but at least one check needs review.
- `go`: all required checks are go.
- Optional live HTTP blocked result is reported as blocked when `--include-live-http` is used, because the caller asked to prove real HTTP access.

## Boundary

The check is read-only except for writing its own JSON/Markdown report files. It does not mutate source catalog, start services, create indexes, call MyPrivateAgent, or promote retrieval behavior.

## Verification

- Unit tests cover go, review, blocked, and CLI exit code mapping.
- Existing approved corpus and local business corpus tests remain the behavior source of truth.
- OpenSpec full validation must pass.
