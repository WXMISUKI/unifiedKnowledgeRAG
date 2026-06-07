# local-rag-http-myprivateagent-call-loop Specification

## Purpose

Define a lightweight closure report proving that the registered local business corpus is usable through live provider HTTP and MyPrivateAgent's caller-side corpus trial.

## Requirements

### Requirement: Local RAG HTTP MyPrivateAgent call loop closure can be exported
The system SHALL export a compact closure report for the local RAG HTTP and MyPrivateAgent caller-side corpus trial loop.

#### Scenario: Local call loop is closed
- **GIVEN** the provider-side usability report has `decision=go` with live HTTP included
- **AND** the MyPrivateAgent caller-side corpus trial has `decision=go`
- **AND** both reports use the same source id
- **WHEN** the closure report is exported
- **THEN** the closure decision is `go`
- **AND** it recommends stopping provider-side readiness work unless a real bug appears

#### Scenario: Local call loop needs review
- **GIVEN** both reports exist and are not blocked
- **WHEN** one report is not `go` or provider live HTTP was not included
- **THEN** the closure decision is `review`
- **AND** it recommends rerunning the missing or weak local trial step

#### Scenario: Local call loop is blocked
- **GIVEN** either report is missing, malformed, blocked, or source ids conflict
- **WHEN** the closure report is exported
- **THEN** the closure decision is `blocked`
- **AND** it records the blocking reason without mutating provider or caller state

### Requirement: Closure remains lightweight
The closure SHALL remain a read-only report over existing trial outputs.

#### Scenario: Closure runs
- **WHEN** the closure report runs
- **THEN** it does not call provider HTTP endpoints, run MyPrivateAgent orchestration, change RAG APIs, change default chat retrieval injection, create source bindings, start services, promote retrieval backends, start OCR, or execute GraphRAG
