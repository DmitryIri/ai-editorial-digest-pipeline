from ai_editorial_digest.models import EnrichedMetadata, RawMetadata


def test_raw_metadata_minimal():
    m = RawMetadata(doi="10.9999/test.001", title="Test Paper")
    assert m.doi == "10.9999/test.001"
    assert m.authors == []
    assert m.keywords == []


def test_raw_metadata_full():
    m = RawMetadata(
        doi="10.9999/test.002",
        title="Full Paper",
        abstract="Abstract text",
        authors=["A. Author"],
        year=2024,
        journal="Test Journal",
        keywords=["nlp", "ai"],
    )
    assert m.year == 2024
    assert len(m.keywords) == 2


def test_enriched_metadata_defaults():
    e = EnrichedMetadata(doi="10.9999/test.003", title="Enriched Paper")
    assert e.enrichment_provider == "mock"
    assert e.ai_keywords == []
    assert e.ai_topics == []


def test_enriched_metadata_roundtrip():
    raw = RawMetadata(doi="10.9999/test.004", title="Roundtrip", keywords=["x"])
    enriched = EnrichedMetadata(
        **raw.model_dump(),
        ai_summary="Summary",
        ai_keywords=["ai-generated", "x"],
        ai_topics=["methodology"],
    )
    d = enriched.model_dump()
    assert d["doi"] == "10.9999/test.004"
    assert d["ai_summary"] == "Summary"
