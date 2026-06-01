## Design Overview

This change adds a read-only Phase 8 live URL validation readiness report that aggregates the minimum evidence chain for deployed URL review.

Core required signals:

1. Phase 8 execution contract
2. Phase 6 deployed field-validation readiness
3. Phase 7 provider release readiness

Optional live signal:

1. deployed provider smoke

## Decisions

- Missing deployed smoke keeps the report in `review` with `await_live_url_validation`.
- Present blocked deployed smoke moves the report to `blocked`.
- `ready` only appears when required signals are ready and deployed smoke is ready with a live URL.
- The readiness report does not imply runtime default promotion.

## Boundaries

- No runtime default promotion
- No new HTTP endpoint
- No retrieval/ingestion/graph execution changes
