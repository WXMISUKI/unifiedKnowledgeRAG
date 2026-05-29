# Change: Evaluate Noisy Identifier Gate Candidate

## Why

The exact identifier gate now handles clean full identifiers, partial identifiers, same-prefix wrong IDs, and multi-ID positives. Real enterprise inputs are less clean: users may type OCR-like `O/0` mistakes, omit hyphens, or use Chinese shorthand for a form/workflow code. A strict exact gate can over-filter these useful hits unless a normalization/alias layer is evaluated.

## What

- Add noisy/alias identifier benchmark fixtures for supported and unsupported cases.
- Add an evaluation-only alias-aware identifier gate candidate that normalizes common local aliases and OCR-like identifiers.
- Export local Qdrant+BGE-M3 evidence comparing the alias-aware candidate on noisy/alias cases.

## Non-Goals

- Do not enable alias-aware gating as a runtime default.
- Do not create a production alias dictionary service.
- Do not change public HTTP contracts or production index schema.
