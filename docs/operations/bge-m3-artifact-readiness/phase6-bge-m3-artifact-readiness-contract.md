# Phase 6 BGE-M3 Artifact Readiness Contract

- Contract ID: `phase6-bge-m3-artifact-readiness-contract-v1`
- Scope: `Phase 6 / Phase 3 Bridge`
- Decision: `evaluation_only_keep_runtime_defaults`

## Purpose

This contract defines how local BGE-M3 model artifacts are validated for deployment review and private-network reuse. It provides artifact evidence only and does not promote runtime defaults by itself.

## Manifest Requirements

`model-manifest.json` is required for BGE-M3 artifact readiness review.

Required manifest fields:

1. `repo_id`, `source`, `model_dir`, `created_at`
2. `local_files_only`
3. `usage` keys:
   - `EMBEDDING_PROVIDER`
   - `EMBEDDING_MODEL_PATH`
   - `EMBEDDING_LOCAL_FILES_ONLY`
   - `EMBEDDING_VECTOR_SIZE`
4. `validation` keys:
   - `required_files`
   - `weight_files`
   - `file_count`
   - `checksums`
   - `checksum_algorithm`

## Artifact Completeness Rules

1. Required files must exist in the model directory:
   - `config.json`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `sentencepiece.bpe.model`
2. At least one model weight file must exist (`*.safetensors` or `*.bin`).
3. `validation.checksum_algorithm` must be `sha256`.
4. `validation.checksums` must cover required files and weight files.

## Deployment Bridge Rules

1. Artifact readiness is deployment evidence, not automatic promotion evidence.
2. Runtime default embedding provider remains unchanged unless a separate promotion gate is approved.
3. For private-network reuse, runtime and manifest should both indicate `local_files_only=true`.
4. Missing or incomplete artifact evidence should stay in `review`/`blocked`, never be auto-corrected by runtime mutation.

## Non-Goals

1. No automatic model download in readiness export.
2. No runtime default switch from `mock` to `bge_m3_local`.
3. No new public HTTP API.
4. No caller control-plane policy changes.
