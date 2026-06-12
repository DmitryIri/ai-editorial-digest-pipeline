# Architecture

## Overview

`ai-editorial-digest-pipeline` is a three-stage data pipeline:

```
DOI list
    │
    ▼
[Fetcher]           ← METADATA_PROVIDER=mock|crossref
    │ RawMetadata (Pydantic)
    ▼
[Enricher]          ← LLM_PROVIDER=mock|openai|anthropic
    │ EnrichedMetadata (Pydantic)
    ▼
[Validator]         ← schema enforcement
    │
    ▼
JSON records + Manifest (SHA-256 checksums)
```

## Modules

### `models.py`
Pydantic v2 models:
- `RawMetadata` — bibliographic record as fetched from source
- `EnrichedMetadata` — record with AI-added fields (`ai_summary`, `ai_keywords`, `ai_topics`)

### `fetcher.py`
Retrieves raw metadata for a DOI.
- `METADATA_PROVIDER=mock` — returns synthetic fixture data (default, no network)
- `METADATA_PROVIDER=crossref` — Crossref REST API (optional live provider, not wired in this public repo)

### `enricher.py`
Adds AI-generated enrichment fields to a `RawMetadata` record.
- `LLM_PROVIDER=mock` — deterministic mock (default, safe for CI)
- `LLM_PROVIDER=openai` — OpenAI chat completions (optional live provider)
- `LLM_PROVIDER=anthropic` — Anthropic Messages API (optional live provider)

### `validator.py`
Enforces required fields on `EnrichedMetadata`. Raises `ValidationError` on invalid records.

### `manifest.py`
Builds a JSON manifest with per-record SHA-256 checksums and a root checksum.
Enables downstream reproducibility checks.

### `pipeline.py`
Orchestrates fetch → enrich → validate → write in a single call.

## Provider-Agnostic Design

The LLM and metadata providers are selected via environment variables.
This allows:
- CI to run fully without API keys (`mock` mode)
- Production deployments to swap providers without code changes
- Easy extension: implement `_enrich_openai()` / `_enrich_anthropic()` in `enricher.py`

## Data Safety

All sample data in `fixtures/` is synthetic. No real DOIs, authors, or article text are included.
