# Change: Add Alias Governance And Split-Chunk Benchmark

## Why

The alias-aware gate passed the noisy local seed, but aliases are still local rules inside code and the benchmark does not show what happens when related identifiers are split across chunks. Before considering runtime promotion, the project needs evidence for alias governance shape and split-chunk false-negative risk.

## What

- Move local alias patterns into an explicit evaluation catalog with owner/status/version/risk metadata.
- Export alias governance evidence so aliases are auditable before production adoption.
- Add a split-chunk fixture source and benchmark cases that expose strict identifier gating risk when multiple identifiers are not co-located in one chunk.
- Document the result as local evidence, not runtime approval.

## Non-Goals

- Do not enable alias normalization or hybrid gating as runtime defaults.
- Do not add a production alias service or database.
- Do not change provider HTTP contracts or production Qdrant schema.
