import json
import tempfile
from pathlib import Path

from ai_editorial_digest.manifest import build_manifest, sha256_dict


def test_sha256_dict_deterministic():
    d = {"doi": "10.9999/test", "title": "Paper"}
    assert sha256_dict(d) == sha256_dict(d)


def test_sha256_dict_differs_for_different_data():
    assert sha256_dict({"a": 1}) != sha256_dict({"a": 2})


def test_build_manifest_creates_file():
    records = [{"doi": "10.9999/test.001", "title": "Paper A"}]
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "manifest.json"
        build_manifest(records, path)
        assert path.exists()
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["record_count"] == 1
        assert len(data["items"]) == 1
        assert data["root_checksum"]


def test_build_manifest_checksum_stability():
    records = [{"doi": "10.9999/test.001", "title": "Paper A"}]
    with tempfile.TemporaryDirectory() as tmpdir:
        path1 = Path(tmpdir) / "m1.json"
        path2 = Path(tmpdir) / "m2.json"
        m1 = build_manifest(records, path1)
        m2 = build_manifest(records, path2)
        assert m1["root_checksum"] == m2["root_checksum"]


def test_build_manifest_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "manifest.json"
        result = build_manifest([], path)
        assert result["record_count"] == 0
        assert result["items"] == []
