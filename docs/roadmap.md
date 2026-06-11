# Roadmap

## Current State (v0.1.0)

- Mock metadata fetching from synthetic fixtures
- Mock LLM enrichment (deterministic, no API calls)
- Pydantic v2 validation
- Per-record JSON output + manifest with SHA-256 checksums
- CI: Python 3.10 / 3.11 / 3.12

## Next Implementation Layer

### Phase 1 — Live Integrations
- [ ] Crossref API: implement `_fetch_crossref()` in `fetcher.py`
- [ ] OpenAI enrichment: implement `_enrich_openai()` in `enricher.py`
- [ ] Anthropic enrichment: implement `_enrich_anthropic()` in `enricher.py`
- [ ] Rate limiting and retry logic for API calls

### Phase 2 — Usability
- [ ] CLI: `python -m ai_editorial_digest enrich dois.txt --output ./out/`
- [ ] Async batch processing for large DOI lists
- [ ] Progress reporting

### Phase 3 — Packaging
- [ ] Docker image
- [ ] `pyproject.toml` entry points
- [ ] PyPI publish
