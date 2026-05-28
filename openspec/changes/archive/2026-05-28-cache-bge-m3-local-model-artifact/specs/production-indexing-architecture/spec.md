## ADDED Requirements

### Requirement: BGE-M3 model artifacts are cached explicitly

The system SHALL provide a repeatable local workflow to download and validate BGE-M3 model artifacts for local and private-network deployment.

#### Scenario: Model artifact is downloaded

- **WHEN** the BGE-M3 download script is run with an output directory
- **THEN** it downloads the configured model snapshot into that directory and writes a local manifest

#### Scenario: Mirror endpoint is configured

- **WHEN** an operator provides a Hugging Face endpoint override
- **THEN** the download workflow uses that endpoint for the download without making it the code default

#### Scenario: Model artifact is validated

- **WHEN** model validation runs
- **THEN** it confirms required config, tokenizer, and model weight files exist before reporting success

#### Scenario: Model binaries remain outside git

- **WHEN** BGE-M3 model artifacts are downloaded locally
- **THEN** model directories are ignored by git and are not committed as repository content
