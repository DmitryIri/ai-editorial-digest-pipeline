# AI Editorial Digest Pipeline

**Turn DOI lists into validated, enriched, audit-ready metadata — a reproducible pipeline for research and publishing workflows.**

Based on patterns from a production editorial system that processes 3 journal issues monthly — cutting a recurring expert task from 6–10 hours to under one hour, with zero pipeline errors. This public repository demonstrates the sanitized metadata-enrichment layer of that system, with synthetic samples and optional live providers.

[![CI](https://github.com/DmitryIri/ai-editorial-digest-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/DmitryIri/ai-editorial-digest-pipeline/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## From Manual Hours to Reproducible Minutes

The source system this repository is patterned on replaced a recurring manual editorial task with an automated, auditable pipeline:

| | Before | After |
|---|---|---|
| Time per issue | 6–10 hours | **under 1 hour** |
| Manual translation/editing passes | 3–5 | **0** |
| Journals covered | 1 (with effort) | **3 simultaneously** |
| Quality | depends on operator and day | **reproducible** (same input → same output) |
| Traceability | none | **full audit trail per run** |

> These outcomes are from the private production system this public repo is patterned on. The public repo demonstrates the sanitized enrichment layer with synthetic samples — it does not reproduce the production run.

---

## What This Pipeline Does

```text
DOI list
    │
    ▼
[Fetch]      retrieve bibliographic metadata for each DOI
    │
    ▼
[Enrich]     add structured AI summary, keywords, and topic tags
    │
    ▼
[Validate]   enforce schema on every enriched record
    │
    ▼
[Output]     per-record JSON  +  manifest with SHA-256 checksums
```

One command turns a list of identifiers into validated, checksummed records ready for downstream ingest — no manual extraction or formatting in between.

---

## Engineered for Trust

This is not a thin wrapper around an LLM. The architecture is designed so the output can be relied on:

- **Reproducible** — deterministic processing; the same input produces the same output.
- **Auditable** — every run produces a manifest with per-record SHA-256 checksums.
- **Validated** — schema enforcement on each record; malformed output fails fast.
- **Provider-agnostic** — metadata and LLM backends swap behind a stable interface, without touching pipeline logic.

These are the properties that turn an AI experiment into a production-grade workflow.

---

## Quick Start

```bash
git clone https://github.com/DmitryIri/ai-editorial-digest-pipeline.git
cd ai-editorial-digest-pipeline
pip install -e ".[dev]"
python examples/quickstart.py
```

Expected output:

```text
Enriched 2 records:

DOI:        10.9999/synthetic.2024.001
Title:      Automated Knowledge Extraction from Scientific Literature
AI Summary: This paper titled 'Automated Knowledge Extraction from
            Scientific Literature' presents research in the domain of
            NLP, knowledge extraction.
AI Topics:  methodology, empirical study
Provider:   mock

Manifest root checksum: 68f60e9684391180...
Records:                2
```

Runs out of the box with no API keys — the default mock provider is CI-safe and deterministic.

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
  "ai_summary": "This paper titled 'Automated Knowledge Extraction from Scientific Literature' presents research in the domain of NLP, knowledge extraction.",
  "ai_keywords": ["ai-generated", "mock", "NLP", "knowledge extraction", "scientific literature"],
  "ai_topics": ["methodology", "empirical study"],
  "enrichment_provider": "mock"
}
```

Manifest with reproducibility checksums:

```json
{
  "generated_at": "2024-01-15T10:30:00+00:00",
  "record_count": 2,
  "items": [{"doi": "10.9999/synthetic.2024.001", "checksum": "sha256..."}],
  "root_checksum": "sha256..."
}
```

---

## Architecture

```text
DOI list
    │
    ▼
[Fetcher]           ← METADATA_PROVIDER=mock | crossref
    │ RawMetadata (Pydantic)
    ▼
[Enricher]          ← LLM_PROVIDER=mock | openai | anthropic
    │ EnrichedMetadata (Pydantic)
    ▼
[Validator]         ← schema enforcement
    │
    ▼
JSON records + Manifest (SHA-256 checksums)
```

A clean separation of concerns: each stage has a typed contract, so backends can change without rewriting the pipeline.

---

## Potential Business Applications

The same pattern — *take an external content stream, turn it into validated, traceable, standardized output* — applies wherever expert time is spent on repeatable extraction and structuring:

- **Research portals** — auto-enrich imported bibliographic records
- **Publishing automation** — metadata completion and quality checks before ingest
- **Literature review / RAG preparation** — structured extraction for downstream pipelines
- **Knowledge graph population** — structured entities from abstracts at scale

---

## Running Tests

```bash
pytest tests/ -v
ruff check src/ tests/ examples/ tools/
```

All tests run on the mock provider — no API keys required. CI runs on Python 3.10 / 3.11 / 3.12.

---

## Project Background

**Problem.** A scientific journal prepared a recurring digest of international research — a monthly task that took a skilled editor 6–10 hours: locate articles, translate, edit to a scientific standard, apply literary editing, and format. Expensive, slow, dependent on scarce expertise, and impossible to scale.

**Solution.** A pipeline that converts a stream of scientific literature into validated, structured editorial output through deterministic, auditable processing — with quality controls and reproducibility built in, and the expert kept on final review rather than manual production.

**Result.** From 6–10 hours to under an hour; from one journal to three simultaneously; production-run in 2026 with outputs delivered to a real editorial team.

**Role.** Sole engineer — architecture, pipeline implementation, validation design, test suite, and the public-safe sanitization that makes this repository shareable without exposing internal systems or private data.

**What this repository is.** The sanitized, provider-agnostic enrichment layer of that system, built to demonstrate the architecture and verification pattern on synthetic data.

---

## Current Scope

This public repository is the **enrichment layer**, packaged as a runnable, CI-safe demonstration:

- **Default mode is mock** — synthetic samples, no API keys, deterministic output. Safe for CI and for running in seconds.
- **Live providers are optional integration points** — `METADATA_PROVIDER=crossref` and `LLM_PROVIDER=openai|anthropic` are defined interfaces ready to be wired to real backends.
- **Sample data in `fixtures/` is synthetic** — no real publications or authors.

The architecture, contracts, validation, and reproducibility pattern are real; the live API backends are the layer left open for adaptation to a specific client's sources and standards.

---

## Stack

- Python 3.10+
- Pydantic v2 — data validation and schema enforcement
- httpx — HTTP client for metadata integration
- ruff — linting · pytest + pytest-cov — testing
- GitHub Actions CI (Python 3.10 / 3.11 / 3.12)

---

## License

MIT
