# Roadmap

## Implemented

The enrichment pipeline runs end to end on the mock provider:

- Metadata fetch through a provider-agnostic interface
- LLM enrichment layer (AI summary, keywords, topic tags)
- Pydantic v2 schema validation on every record
- Per-record JSON output + manifest with SHA-256 checksums
- CI on Python 3.10 / 3.11 / 3.12

## Optional Integration Points

The architecture exposes clean extension points for a production adaptation. They are intentionally left open so the public repository stays CI-safe and key-free:

- **Live metadata** — wire `METADATA_PROVIDER=crossref` to the Crossref REST API
- **Live enrichment** — wire `LLM_PROVIDER=openai` or `anthropic` to a real backend
- **Batch CLI** for large DOI lists
- **Containerized packaging**

Each is an interface already defined in the codebase, ready to connect to a specific client's sources and editorial standards without changing the validated output contract.
