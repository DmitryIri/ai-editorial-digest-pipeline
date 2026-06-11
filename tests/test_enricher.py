import pytest

from ai_editorial_digest.enricher import enrich
from ai_editorial_digest.models import EnrichedMetadata, RawMetadata


def _sample_raw(**kwargs) -> RawMetadata:
    defaults = dict(
        doi="10.9999/test.001",
        title="Test Paper",
        abstract="Abstract text",
        keywords=["nlp", "ai"],
    )
    defaults.update(kwargs)
    return RawMetadata(**defaults)


def test_enrich_mock_returns_enriched(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    result = enrich(_sample_raw())
    assert isinstance(result, EnrichedMetadata)
    assert result.enrichment_provider == "mock"


def test_enrich_mock_summary_present(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    result = enrich(_sample_raw())
    assert result.ai_summary
    assert "Test Paper" in result.ai_summary


def test_enrich_mock_keywords_include_original(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    result = enrich(_sample_raw(keywords=["ecology"]))
    assert "ecology" in result.ai_keywords


def test_enrich_mock_topics_present(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    result = enrich(_sample_raw())
    assert len(result.ai_topics) > 0


def test_enrich_invalid_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "bad_provider")
    with pytest.raises(ValueError, match="Unknown LLM_PROVIDER"):
        enrich(_sample_raw())


def test_enrich_openai_stub(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    with pytest.raises(NotImplementedError):
        enrich(_sample_raw())


def test_enrich_anthropic_stub(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    with pytest.raises(NotImplementedError):
        enrich(_sample_raw())
