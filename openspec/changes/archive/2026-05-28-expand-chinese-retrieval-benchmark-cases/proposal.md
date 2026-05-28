# Change: expand-chinese-retrieval-benchmark-cases

## Summary

Expand the local retrieval benchmark fixture with more Chinese enterprise RAG cases before evaluating real embedding models or promoting Qdrant.

## Motivation

The current benchmark set proves the harness contract, but it is still too small to guide Chinese-heavy embedding and vector-store decisions. The next model-selection discussion needs representative questions that exercise policy exceptions, evidence requirements, paraphrases, cross-source retrieval, operational terms, and expected empty answers.

This change keeps the scope local and deterministic: extend source fixtures, fixture retrieval chunks, benchmark cases, focused tests, and documentation. It does not add real embedding providers or change the default backend.

## Goals

- Add Chinese-heavy benchmark cases that represent enterprise support workflows.
- Cover additional categories such as exception policy, operational escalation, SLA/timeliness, cross-source evidence, and hard empty cases.
- Keep fixture backend deterministic so benchmark evidence remains stable before real embedding adapters exist.
- Document that this benchmark set is a seed corpus, not final production acceptance coverage.

## Non-Goals

- Do not select or implement a real embedding model.
- Do not promote Qdrant as the default backend.
- Do not add external datasets or network dependencies.
- Do not add public benchmark HTTP APIs.
