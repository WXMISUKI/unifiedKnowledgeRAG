import json

from scripts.download_bge_m3_model import (
    download_bge_m3_model,
    validate_bge_m3_model_dir,
)


def _write_minimal_model_files(model_dir):
    model_dir.mkdir(parents=True, exist_ok=True)
    for filename in (
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json",
        "sentencepiece.bpe.model",
        "model.safetensors",
    ):
        (model_dir / filename).write_text("fixture", encoding="utf-8")


def test_validate_bge_m3_model_dir_accepts_required_files(tmp_path):
    model_dir = tmp_path / "bge-m3"
    _write_minimal_model_files(model_dir)

    validation = validate_bge_m3_model_dir(model_dir)

    assert validation["file_count"] == 5
    assert validation["weight_files"] == ["model.safetensors"]
    assert validation["checksum_algorithm"] == "sha256"
    assert len(validation["checksums"]) == 5


def test_validate_bge_m3_model_dir_rejects_missing_files(tmp_path):
    model_dir = tmp_path / "bge-m3"
    model_dir.mkdir()
    (model_dir / "config.json").write_text("{}", encoding="utf-8")

    try:
        validate_bge_m3_model_dir(model_dir)
    except FileNotFoundError as error:
        assert "tokenizer.json" in str(error)
        assert "*.safetensors or *.bin" in str(error)
    else:
        raise AssertionError("Expected incomplete BGE-M3 artifact to be rejected")


def test_download_bge_m3_model_writes_manifest_without_network_when_skipped(tmp_path):
    model_dir = tmp_path / "bge-m3"
    _write_minimal_model_files(model_dir)

    manifest_path = download_bge_m3_model(
        output_dir=model_dir,
        hf_endpoint="https://hf-mirror.com",
        local_files_only=True,
        skip_download=True,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["repo_id"] == "BAAI/bge-m3"
    assert manifest["source"] == "huggingface"
    assert manifest["hf_endpoint"] == "https://hf-mirror.com"
    assert manifest["local_files_only"] is True
    assert manifest["usage"]["EMBEDDING_PROVIDER"] == "bge_m3_local"
    assert manifest["usage"]["EMBEDDING_LOCAL_FILES_ONLY"] == "true"
    assert manifest["validation"]["checksum_algorithm"] == "sha256"
    assert "config.json" in manifest["validation"]["checksums"]


def test_download_bge_m3_model_uses_snapshot_download(monkeypatch, tmp_path):
    calls = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        _write_minimal_model_files(tmp_path / "bge-m3")

    import sys
    from types import SimpleNamespace

    monkeypatch.setitem(
        sys.modules,
        "huggingface_hub",
        SimpleNamespace(snapshot_download=fake_snapshot_download),
    )

    manifest_path = download_bge_m3_model(
        repo_id="BAAI/bge-m3",
        output_dir=tmp_path / "bge-m3",
        revision="main",
        local_files_only=False,
    )

    assert manifest_path.exists()
    assert calls == [
        {
            "repo_id": "BAAI/bge-m3",
            "revision": "main",
            "local_dir": str((tmp_path / "bge-m3").resolve()),
            "local_dir_use_symlinks": False,
            "local_files_only": False,
        }
    ]


def test_download_bge_m3_model_uses_modelscope_snapshot(monkeypatch, tmp_path):
    calls = []

    def fake_snapshot_download(**kwargs):
        calls.append(kwargs)
        _write_minimal_model_files(tmp_path / "bge-m3")

    import sys
    from types import SimpleNamespace

    monkeypatch.setitem(sys.modules, "modelscope", SimpleNamespace())
    monkeypatch.setitem(sys.modules, "modelscope.hub", SimpleNamespace())
    monkeypatch.setitem(
        sys.modules,
        "modelscope.hub.snapshot_download",
        SimpleNamespace(snapshot_download=fake_snapshot_download),
    )

    manifest_path = download_bge_m3_model(
        repo_id="BAAI/bge-m3",
        output_dir=tmp_path / "bge-m3",
        source="modelscope",
        revision="master",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["source"] == "modelscope"
    assert calls == [
        {
            "model_id": "BAAI/bge-m3",
            "revision": "master",
            "local_dir": str((tmp_path / "bge-m3").resolve()),
        }
    ]
