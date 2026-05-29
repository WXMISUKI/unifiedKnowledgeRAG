## Context

The prompt package boundary captures query, allowed citations, and evidence, but it stops short of rendering a model-ready prompt structure. If future Qwen, OpenAI, or local LLM adapters each render messages independently, the project will risk prompt drift and inconsistent citation constraints.

This change adds a deterministic renderer owned by the provider. It does not expose the full rendered prompt as a public API and does not call any model.

## Goals / Non-Goals

**Goals:**
- Render prompt packages into a stable chat-style message list.
- Include compact renderer metadata in answered results.
- Keep prompt rendering provider-neutral and reusable by future composers.
- Preserve existing deterministic answer output.

**Non-Goals:**
- Add a hosted/local LLM adapter.
- Expose full prompt text in `/api/rag/answer`.
- Add provider-specific prompt templates, streaming messages, or token counting.

## Decisions

1. Use chat-style messages internally.

   Rationale: both hosted chat APIs and local chat runtimes can adapt from role/content messages more easily than from a single free-form string.

2. Expose only renderer summary metadata.

   Rationale: callers need auditability, but exact prompt wording should remain an internal provider implementation detail.

3. Keep renderer deterministic and dependency-free.

   Rationale: this should remain testable in local CI without model or tokenizer dependencies.

## Risks / Trade-offs

- No token budget management yet -> This is deferred until real model context limits are selected.
- Prompt wording can still evolve -> The public metadata tracks renderer id and message count rather than exact message text.
