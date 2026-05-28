# Design: cache-bge-m3-local-model-artifact

## Approach

Add `scripts/download_bge_m3_model.py` as the canonical local bootstrap command. It uses `huggingface_hub.snapshot_download` and writes a small `model-manifest.json` into the target directory.

Default behavior:

- repo id: `BAAI/bge-m3`
- output dir: `models/bge-m3`
- endpoint: normal Hugging Face unless `--hf-endpoint` or `HF_ENDPOINT` is configured
- validation: required model/config/tokenizer files must exist

## Local Artifact Policy

`models/` is ignored by git. The manifest is also local-only because it describes the local downloaded artifact and may differ by revision or download time.

Future private-network deployment can copy `models/bge-m3` and set:

```powershell
$env:EMBEDDING_MODEL_PATH="D:\models\bge-m3"
$env:EMBEDDING_LOCAL_FILES_ONLY="true"
```

## Safety

Tests should exercise script argument handling and validation using temporary fixture directories, not by downloading the real model. The actual download is a post-implementation operational step.
