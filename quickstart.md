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
