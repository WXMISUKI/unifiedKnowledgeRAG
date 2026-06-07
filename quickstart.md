# Start the local provider

```powershell
conda activate GRAPHRAG
uvicorn app.main:app --reload --port 8020
```

# Verify the local usable run-loop

Run this in another terminal after the provider is listening on port 8020:

```powershell
conda activate GRAPHRAG
python scripts/export_local_usable_run_loop.py --base-url http://127.0.0.1:8020
```

Default outputs:

```text
docs/local-run/local-usable-run-loop.json
docs/local-run/local-usable-run-loop.md
```

`Decision: go` means the local provider is usable for discovery, preflight,
retrieval evidence, and a cited answer. `review` means the local fixture query,
source id, or corpus needs review. `blocked` means the provider or contract path
must be fixed before local caller integration.

# Try a PDF-derived markdown corpus

Raw PDF ingestion is not supported by the provider yet. For a small local trial,
convert the first pages of a PDF into a markdown artifact and evaluate that
derived text:

```powershell
python scripts/export_pdf_derived_markdown_trial.py `
  --pdf-path "D:\xwechat_files\wxid_pc6sc451nt9022_dea0\msg\file\2026-06\公司简介2025年10月27日(1).pdf" `
  --max-pages 5 `
  --query "公司主营业务是什么？"
```

Default outputs:

```text
docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md
docs/local-run/pdf-derived-corpus/pdf-derived-markdown-trial.json
docs/local-run/pdf-derived-corpus/pdf-derived-markdown-trial.md
```

If the current Python environment does not have a PDF text extractor, use an
environment with `pypdf` or run external OCR/Layout first and keep the provider
focused on the derived markdown.

# Try a local business markdown corpus

After a markdown artifact is available, run a local business corpus trial before
formal source registration:

```powershell
python scripts/export_local_business_corpus_trial.py `
  --markdown-path docs/local-run/pdf-derived-corpus/company_profile_2025_trial.md `
  --source-id company_profile_2025_trial `
  --title "公司简介 2025 trial" `
  --query "公司主营业务是什么？"
```

Default outputs:

```text
docs/local-run/business-corpus-trial/local-business-corpus-source.json
docs/local-run/business-corpus-trial/local-business-corpus-chunks.json
docs/local-run/business-corpus-trial/local-business-corpus-trial.json
docs/local-run/business-corpus-trial/local-business-corpus-trial.md
```

This is a pre-registration trial. It does not modify the default source catalog
or expose the trial source through provider HTTP APIs.

# Export caller handoff for local corpus

When the local business corpus trial is `go`, package it for caller review:

```powershell
python scripts/export_local_corpus_caller_handoff.py `
  --trial-report docs/local-run/business-corpus-trial/local-business-corpus-trial.json
```

Default outputs:

```text
docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.json
docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.md
```

`ready_for_caller_review` means the caller can review the local artifacts before
formal binding or source registration. It is not production registration.

# Register approved local corpus source

After caller review, explicitly register the handoff as a local provider source:

```powershell
python scripts/register_approved_local_corpus_source.py `
  --handoff docs/local-run/corpus-caller-handoff/local-corpus-caller-handoff.json
```

Default outputs:

```text
app/data/local_sources/approved_sources.json
app/data/sources/company_profile_2025_trial.md
docs/local-run/approved-local-source-registration/approved-local-source-registration.json
docs/local-run/approved-local-source-registration/approved-local-source-registration.md
```

After registration, `company_profile_2025_trial` is visible to
`GET /api/rag/sources` and can be used by `POST /api/rag/retrieve` and
`POST /api/rag/answer`. This is still local provider source registration; it
does not create source-to-agent binding, formal ingestion jobs, OCR startup,
backend promotion, MyPrivateAgent orchestration, or GraphRAG execution.
