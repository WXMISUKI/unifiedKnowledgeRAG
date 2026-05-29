## Why

Answer output validation now checks a citation list, but future hosted/local LLM composers will first produce answer text. The provider needs a shared parser boundary that extracts cited answer text and citations before validation so model adapters do not each invent their own parsing rules.

## What Changes

- Add a deterministic cited answer output parser.
- Extract bracketed citations from answer text in first-seen order.
- Route deterministic composer output through the parser before validation.
- Attach compact parser metadata to answered results.
- Preserve existing answer text, output validation behavior, and fail-closed hosted/local composers.

## Capabilities

### New Capabilities

### Modified Capabilities
- `document-rag`: Adds cited answer output parsing metadata and parser boundary before validation.

## Impact

- Runtime: adds parser service and uses it in deterministic answer composition.
- Contracts: enriches answer metadata with output parser details.
- Tests: verifies parser extraction and missing-citation behavior.
- Docs: updates README answer composer notes.
