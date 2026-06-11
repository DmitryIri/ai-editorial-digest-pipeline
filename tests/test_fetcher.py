
import pytest

from ai_editorial_digest.fetcher import fetch_metadata
from ai_editorial_digest.models import RawMetadata


def test_fetch_known_doi(monkeypatch):
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    result = fetch_metadata("10.9999/synthetic.2024.001")
    assert isinstance(result, RawMetadata)
    assert result.doi == "10.9999/synthetic.2024.001"
    assert "Automated Knowledge Extraction" in result.title
    assert result.year == 2024


def test_fetch_unknown_doi_fallback(monkeypatch):
    monkeypatch.setenv("METADATA_PROVIDER", "mock")
    result = fetch_metadata("10.9999/does.not.exist.999")
    assert isinstance(result, RawMetadata)
    assert result.doi == "10.9999/does.not.exist.999"
    assert result.title  # has fallback title


def test_fetch_invalid_provider(monkeypatch):
    monkeypatch.setenv("METADATA_PROVIDER", "unknown_provider")
    with pytest.raises(ValueError, match="Unknown METADATA_PROVIDER"):
        fetch_metadata("10.9999/any.doi")


def test_fetch_crossref_stub(monkeypatch):
    monkeypatch.setenv("METADATA_PROVIDER", "crossref")
    with pytest.raises(NotImplementedError):
        fetch_metadata("10.9999/any.doi")
