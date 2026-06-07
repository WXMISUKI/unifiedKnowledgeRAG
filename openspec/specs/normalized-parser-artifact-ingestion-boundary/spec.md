# normalized-parser-artifact-ingestion-boundary Specification

## Purpose
TBD - created by archiving change add-normalized-parser-artifact-ingestion-boundary. Update Purpose after archive.
## Requirements
### Requirement: Normalized parser artifact can be validated
The system SHALL validate externally produced parser artifacts before they are allowed to enter the local RAG ingestion path.

#### Scenario: Ready artifact is accepted
- **WHEN** a parser artifact includes artifact id, source id, title, original file metadata, parser metadata, non-empty text blocks, stable provenance, and at least one citation anchor
- **THEN** the artifact validation report has `decision=go`
- **AND** it records source id, artifact id, parser id, original file path, content digest, text block count, citation count, and recommended next action

#### Scenario: Artifact missing required text is blocked
- **WHEN** a parser artifact has no non-empty text blocks
- **THEN** the artifact validation report has `decision=blocked`
- **AND** it records `reason_code=artifact_has_no_text_blocks`

#### Scenario: Artifact missing citation anchors needs review
- **WHEN** a parser artifact has source identity and non-empty text blocks but no citation anchors
- **THEN** the artifact validation report has `decision=review`
- **AND** it records `reason_code=artifact_missing_citation_anchors`

#### Scenario: Raw source file is not treated as an artifact
- **WHEN** the input path points to a raw PDF, Word, Excel, or image file instead of a normalized parser artifact JSON file
- **THEN** the artifact validation report has `decision=blocked`
- **AND** it records that external parser output is required before provider ingestion

### Requirement: Ready parser artifact can be materialized for existing ingestion loop
The system SHALL materialize a ready normalized parser artifact into provider-managed markdown and source overlay files that are compatible with the existing local source onboarding and approved-source ingestion loops.

#### Scenario: Ready artifact is materialized
- **WHEN** a parser artifact validation report has `decision=go`
- **THEN** the exporter writes deterministic markdown and source overlay artifacts under a local-run output directory
- **AND** the report records the generated markdown path, overlay path, source id, artifact id, content digest, and recommended onboarding command

#### Scenario: Review artifact is not materialized as ready
- **WHEN** a parser artifact validation report has `decision=review`
- **THEN** the exporter does not claim ingestion readiness
- **AND** it records the review reason and recommended artifact fixes

#### Scenario: Blocked artifact is not materialized
- **WHEN** a parser artifact validation report has `decision=blocked`
- **THEN** the exporter does not write provider-managed source material
- **AND** the command exits non-zero when used as a CLI

### Requirement: Parser artifact boundary remains lightweight
The parser artifact boundary SHALL preserve external parser ownership and avoid promoting heavier runtime behavior.

#### Scenario: Artifact boundary runs
- **WHEN** the validation or materialization command runs
- **THEN** it does not parse raw PDFs
- **AND** it does not start OCR services
- **AND** it does not call PaddleOCR or other parser engines
- **AND** it does not create source-to-agent bindings
- **AND** it does not call MyPrivateAgent
- **AND** it does not create ingestion jobs
- **AND** it does not promote retrieval backend defaults
- **AND** it does not call vector databases
- **AND** it does not execute GraphRAG

