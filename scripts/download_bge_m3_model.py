import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path


DEFAULT_REPO_ID = "BAAI/bge-m3"
DEFAULT_OUTPUT_DIR = Path("models/bge-m3")
SUPPORTED_SOURCES = {"huggingface", "modelscope"}
MANIFEST_NAME = "model-manifest.json"
REQUIRED_FILES = (
    "config.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "sentencepiece.bpe.model",
)
MODEL_WEIGHT_SUFFIXES = (".safetensors", ".bin")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and validate a local BGE-M3 model artifact."
    )
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument(
        "--source",
        choices=sorted(SUPPORTED_SOURCES),
        default="huggingface",
        help="Model hub source used for download.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Local target directory for the model snapshot.",
    )
    parser.add_argument(
        "--revision",
        default=None,
        help="Optional Hugging Face model revision.",
    )
    parser.add_argument(
        "--hf-endpoint",
        default=None,
        help="Optional Hugging Face-compatible endpoint, e.g. https://hf-mirror.com.",
    )
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        help="Validate/use local cache only; do not download from network.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Only validate an existing output directory and write manifest.",
    )
    return parser.parse_args()


def download_bge_m3_model(
    repo_id: str = DEFAULT_REPO_ID,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    source: str = "huggingface",
    revision: str | None = None,
    hf_endpoint: str | None = None,
    local_files_only: bool = False,
    skip_download: bool = False,
) -> Path:
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    endpoint = hf_endpoint or os.getenv("HF_ENDPOINT")
    if endpoint:
        os.environ["HF_ENDPOINT"] = endpoint

    if source not in SUPPORTED_SOURCES:
        raise ValueError(f"Unsupported BGE-M3 model source: {source}")

    if not skip_download:
        if source == "huggingface":
            _download_from_huggingface(
                repo_id=repo_id,
                output_dir=output_dir,
                revision=revision,
                local_files_only=local_files_only,
            )
        else:
            _download_from_modelscope(
                repo_id=repo_id,
                output_dir=output_dir,
                revision=revision,
            )

    validation = validate_bge_m3_model_dir(output_dir)
    manifest_path = write_manifest(
        output_dir=output_dir,
        repo_id=repo_id,
        source=source,
        revision=revision,
        hf_endpoint=endpoint,
        local_files_only=local_files_only,
        validation=validation,
    )
    return manifest_path


def _download_from_huggingface(
    repo_id: str,
    output_dir: Path,
    revision: str | None,
    local_files_only: bool,
) -> None:
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id=repo_id,
        revision=revision,
        local_dir=str(output_dir),
        local_dir_use_symlinks=False,
        local_files_only=local_files_only,
    )


def _download_from_modelscope(
    repo_id: str,
    output_dir: Path,
    revision: str | None,
) -> None:
    from modelscope.hub.snapshot_download import snapshot_download

    snapshot_download(
        model_id=repo_id,
        revision=revision,
        local_dir=str(output_dir),
    )


def validate_bge_m3_model_dir(model_dir: Path) -> dict:
    missing = [
        filename
        for filename in REQUIRED_FILES
        if not (model_dir / filename).is_file()
    ]
    weight_files = sorted(
        path.name
        for path in model_dir.iterdir()
        if path.is_file() and path.suffix in MODEL_WEIGHT_SUFFIXES
    )
    if not weight_files:
        missing.append("*.safetensors or *.bin")

    if missing:
        raise FileNotFoundError(
            "BGE-M3 model artifact is incomplete. Missing: "
            + ", ".join(missing)
        )

    return {
        "required_files": list(REQUIRED_FILES),
        "weight_files": weight_files,
        "file_count": sum(1 for path in model_dir.rglob("*") if path.is_file()),
    }


def write_manifest(
    output_dir: Path,
    repo_id: str,
    source: str,
    revision: str | None,
    hf_endpoint: str | None,
    local_files_only: bool,
    validation: dict,
) -> Path:
    manifest = {
        "repo_id": repo_id,
        "source": source,
        "revision": revision,
        "model_dir": str(output_dir),
        "hf_endpoint": hf_endpoint,
        "local_files_only": local_files_only,
        "created_at": datetime.now(UTC).isoformat(),
        "validation": validation,
        "usage": {
            "EMBEDDING_PROVIDER": "bge_m3_local",
            "EMBEDDING_MODEL_PATH": str(output_dir),
            "EMBEDDING_LOCAL_FILES_ONLY": "true",
            "EMBEDDING_VECTOR_SIZE": "1024",
        },
    }
    manifest_path = output_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return manifest_path


def main() -> None:
    args = parse_args()
    manifest_path = download_bge_m3_model(
        repo_id=args.repo_id,
        output_dir=args.output_dir,
        source=args.source,
        revision=args.revision,
        hf_endpoint=args.hf_endpoint,
        local_files_only=args.local_files_only,
        skip_download=args.skip_download,
    )
    print(f"BGE-M3 model artifact ready: {manifest_path}")


if __name__ == "__main__":
    main()
