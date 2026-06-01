## Overview

This change adds a single read-only protocol document that standardizes how Phase 3 retrieval candidates should be reviewed before any promotion request. The document is intentionally local and lightweight: it consolidates gate intent and evidence requirements without adding code paths or runtime switches.

## Design Goals

1. Give reviewers one place to understand candidate evaluation expectations.
2. Prevent accidental runtime promotion based on isolated positive metrics.
3. Keep candidate evaluation evidence aligned with existing Phase 3 readiness exports and handoff summaries.

## Document Structure

The protocol document contains:

- Scope and non-goals.
- Candidate gate matrix (Qdrant, BGE-M3, hybrid retrieval, hybrid gating, aggregation, relation-aware grading, deployed smoke).
- Required evidence families per gate:
  - customer-like benchmark coverage
  - FP/FN review
  - latency/deployment diagnostics
  - deployed URL smoke follow-up
- Promotion decision rule:
  - candidate evidence can advance review quality
  - runtime defaults remain unchanged until gates are explicitly closed by separate changes

## Non-Goals

- No retrieval backend switch.
- No embedding model promotion.
- No GraphRAG execution implementation.
- No parser expansion.
- No new HTTP API.
