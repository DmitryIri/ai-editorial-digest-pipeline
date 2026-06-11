# ai-editorial-digest-pipeline

**Enrich bibliographic metadata with LLMs: structured summaries, keywords, and topic tags from DOI lists.**

Takes a DOI list, fetches bibliographic metadata, and uses an LLM to add AI-generated summaries, keywords, and topic tags — output is validated JSON with per-record checksums.

[![CI](https://github.com/DmitryIri/ai-editorial-digest-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/DmitryIri/ai-editorial-digest-pipeline/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What It Solves

Research and publishing teams maintain bibliographic databases that are incomplete or inconsistently structured. Manual enrichment is expensive; rule-based parsing fails on free-text abstracts.

This pipeline automates the enrichment step:

1. **Fetch** — retrieve bibliographic metadata for a DOI list (Crossref-style)
2. **Enrich** — pass each abstract through an LLM to extract structured fields
3. **Validate** — enforce schema on enriched output
4. **Output** — write validated JSON records + manifest with SHA-256 checksums

> Portfolio project demonstrating LLM integration, provider-agnostic architecture, structured output validation, and reproducible pipeline design. All sample data is synthetic.

---

## Current Scope

- DOI list → metadata fetch (mock provider; Crossref stub ready to extend)
- LLM enrichment: AI summary, keywords, topic tags
- Provider-agnostic LLM layer: `LLM_PROVIDER=mock|openai|anthropic`
- Per-record JSON output + manifest with SHA-256 checksums
- 100% mock-based tests — no API keys required for CI

---

## Potential Business Applications

- **Research portals:** auto-enrich imported bibliographic records
- **Literature review tools:** structured extraction for downstream RAG pipelines
- **Publishing automation:** metadata completion and quality checks before ingest
- **Knowledge graph population:** extract structured entities from abstracts at scale

---

## Quick Start

```bash
git clone https://github.com/DmitryIri/ai-editorial-digest-pipeline.git
cd ai-editorial-digest-pipeline
pip install -e ".[dev]"
python examples/quickstart.py
```

Expected output:

```
Enriched 2 records:

DOI:        10.9999/synthetic.2024.001
Title:      Automated Knowledge Extraction from Scientific Literature
AI Summary: This paper presents a framework for automated extraction of structured
            knowledge entities from scientific abstracts, demonstrating improved
            precision over rule-based baselines on a synthetic benchmark dataset.
AI Topics:  methodology, empirical study
Provider:   mock

DOI:        10.9999/synthetic.2024.002
Title:      LLM-Assisted Metadata Enrichment in Digital Libraries
AI Summary: This paper examines large language models for enriching incomplete
            bibliographic records in digital library systems, evaluating quality
            using controlled synthetic benchmarks with ground-truth annotations.
AI Topics:  methodology, empirical study
Provider:   mock

Manifest root checksum: 68f60e9684391180...
Records:                2
```

---

## Architecture

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

---

## Output Format

Each enriched record:

```json
{
  "doi": "10.9999/synthetic.2024.001",
  "title": "Automated Knowledge Extraction from Scientific Literature",
  "abstract": "We present a synthetic study on automated extraction of structured knowledge...",
  "authors": ["Alice Researcher", "Bob Scholar"],
  "year": 2024,
  "journal": "Journal of Synthetic Research",
  "keywords": ["NLP", "knowledge extraction"],
  "ai_summary": "This paper presents a framework for automated extraction of structured knowledge entities from scientific abstracts, achieving higher precision than rule-based approaches on the benchmark dataset.",
  "ai_keywords": ["knowledge-extraction", "NLP", "scientific-literature", "information-retrieval"],
  "ai_topics": ["methodology", "empirical study"],
  "enrichment_provider": "mock"
}
```

Manifest:

```json
{
  "generated_at": "2024-01-15T10:30:00+00:00",
  "record_count": 2,
  "items": [{"doi": "10.9999/synthetic.2024.001", "checksum": "sha256..."}],
  "root_checksum": "sha256..."
}
```

---

## Running Tests

```bash
pytest tests/ -v
```

All tests use `LLM_PROVIDER=mock` — no API keys required.

```bash
ruff check src/ tests/ examples/ tools/
```

---

## Next Implementation Layer

- [ ] Live Crossref API integration (`METADATA_PROVIDER=crossref`)
- [ ] Real LLM enrichment: OpenAI and Anthropic backends (stubs are ready to fill)
- [ ] Async batch processing for large DOI lists
- [ ] CLI: `python -m ai_editorial_digest enrich dois.txt`
- [ ] Docker packaging

---

## Stack

- Python 3.10+
- Pydantic v2 (data validation and schema enforcement)
- httpx (HTTP client — ready for Crossref integration)
- ruff (linting)
- pytest + pytest-cov (testing)
- GitHub Actions CI (Python 3.10 / 3.11 / 3.12)

---

## Project Background

**Problem:** Bibliographic metadata in research systems is often incomplete — missing summaries, inconsistent keywords, no topic classification. LLM-assisted enrichment can add these fields at scale, but requires a structured, validated pipeline rather than ad-hoc scripting.

**Stack:** Python pipeline with Pydantic v2 validation, provider-agnostic LLM layer, manifest generation with SHA-256 checksums for reproducibility and auditability.

**Role:** Architecture design, pipeline implementation, LLM integration design, test suite.

**Outcome:** Runnable proof-of-concept demonstrating structured LLM output, API integration patterns, and data pipeline reproducibility — directly applicable to publishing automation, RAG data preparation, and research database enrichment.

---

## Scope Caveats

- Crossref and LLM backends (OpenAI, Anthropic) are stubs in this portfolio version — the integration interfaces are defined, not implemented
- All sample data in `fixtures/` is synthetic — no real publications or authors
- This is a portfolio project / proof-of-concept, not production software

---

## License

MIT
