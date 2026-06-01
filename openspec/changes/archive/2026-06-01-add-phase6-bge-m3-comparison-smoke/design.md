## Summary

Add a lightweight smoke artifact that checks whether the BGE-M3 comparison review chain is locally complete and parseable.

## Phase Alignment

- Roadmap phase: Phase 6 operations with Phase 3 bridge support.
- Nature: read-only smoke evidence maintenance.
- Non-goal: executing embeddings, running Qdrant, or changing runtime defaults.

## Smoke Checks

- Comparison contract exists.
- Comparison diagnostics export exists and is parseable.
- BGE-M3 artifact readiness export exists and is parseable.
- Phase 3 runtime and latency diagnostics are present.
- Deployment readiness evidence is present.

## Output

- `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.json`
- `docs/smoke/bge-m3-comparison/phase6-bge-m3-comparison-smoke.md`
