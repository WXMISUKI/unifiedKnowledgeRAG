# Phase 2 Parser Expansion Demand Contract

## Purpose

This contract defines when parser expansion beyond Markdown should be proposed in this provider.

## Current Baseline

- Default parser baseline: `markdown`
- Deferred parser families: `pdf`, `word`, `excel`, `ocr`, `table-structure`
- Current posture: `keep_markdown_baseline`

## Required Evidence Before Expansion

1. Real source-format demand is visible from source package and ingestion evidence.
2. Unsupported format distribution is visible across current corpus snapshots.
3. Candidate parser quality review (FP/FN) scope is explicitly documented.
4. Candidate parser latency/resource/deployment impact review is explicitly documented.

## Review Expectations

- Parser expansion is evidence-gated, not roadmap-theory-gated.
- Each parser family should be introduced by an independent, evidence-backed OpenSpec change.
- Local evidence exports and smoke artifacts are review inputs only and do not imply runtime promotion.

## Non-Goals

- Enabling non-Markdown parser runtime behavior in this slice.
- Adding OCR services, office parsing dependencies, or table extraction pipelines.
- Changing ingestion execution flow, retrieval defaults, or control-plane ownership boundaries.
