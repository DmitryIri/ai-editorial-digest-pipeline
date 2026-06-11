import json
import tempfile
from pathlib import Path

from ai_editorial_digest.pipeline import run_pipeline

SYNTHETIC_DOIS = [
    "10.9999/synthetic.2024.001",
    "10.9999/synthetic.2024.002",
]


def test_pipeline_runs_and_returns_records(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    with tempfile.TemporaryDirectory() as tmpdir:
        records = run_pipeline(SYNTHETIC_DOIS, output_dir=Path(tmpdir))
    assert len(records) == 2
    for r in records:
        assert r["doi"]
        assert r["title"]
        assert r["ai_summary"]
        assert r["enrichment_provider"] == "mock"


def test_pipeline_writes_json_files(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir)
        run_pipeline(SYNTHETIC_DOIS, output_dir=out)
        json_files = list(out.glob("*.json"))
        # 2 record files + 1 manifest
        assert len(json_files) == 3


def test_pipeline_writes_manifest(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    with tempfile.TemporaryDirectory() as tmpdir:
        out = Path(tmpdir)
        run_pipeline(SYNTHETIC_DOIS, output_dir=out)
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["record_count"] == 2
        assert manifest["root_checksum"]


def test_pipeline_single_doi(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    with tempfile.TemporaryDirectory() as tmpdir:
        records = run_pipeline(["10.9999/synthetic.2024.001"], output_dir=Path(tmpdir))
    assert len(records) == 1


def test_pipeline_empty_list(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    with tempfile.TemporaryDirectory() as tmpdir:
        records = run_pipeline([], output_dir=Path(tmpdir))
    assert records == []
