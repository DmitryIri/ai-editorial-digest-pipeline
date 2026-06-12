from __future__ import annotations

import os

from .models import EnrichedMetadata, RawMetadata


def enrich(metadata: RawMetadata) -> EnrichedMetadata:
    """Enrich metadata using an LLM provider.

    LLM_PROVIDER env var controls the backend:
      - 'mock' (default): deterministic synthetic enrichment — no API calls, safe for CI
      - 'openai': OpenAI chat completion (optional live provider, requires OPENAI_API_KEY)
      - 'anthropic': Anthropic Messages API (optional live provider, requires ANTHROPIC_API_KEY)
    """
    provider = os.getenv("LLM_PROVIDER", "mock")
    if provider == "mock":
        return _enrich_mock(metadata)
    elif provider == "openai":
        return _enrich_openai(metadata)
    elif provider == "anthropic":
        return _enrich_anthropic(metadata)
    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER: {provider!r}. Use 'mock', 'openai', or 'anthropic'."
        )


def _enrich_mock(metadata: RawMetadata) -> EnrichedMetadata:
    """Deterministic mock enrichment — no LLM calls. Used in CI and demos."""
    domain_hint = ", ".join(metadata.keywords[:2]) if metadata.keywords else "general science"
    return EnrichedMetadata(
        **metadata.model_dump(),
        ai_summary=(
            f"This paper titled '{metadata.title}' "
            f"presents research in the domain of {domain_hint}."
        ),
        ai_keywords=["ai-generated", "mock", *(metadata.keywords[:3])],
        ai_topics=["methodology", "empirical study"],
        enrichment_provider="mock",
    )


def _enrich_openai(metadata: RawMetadata) -> EnrichedMetadata:
    """Enrich via OpenAI chat completions (optional live provider)."""
    raise NotImplementedError(
        "OpenAI is an optional live provider and is not wired in this public repo. "
        "Use LLM_PROVIDER=mock (default) to run without API keys."
    )


def _enrich_anthropic(metadata: RawMetadata) -> EnrichedMetadata:
    """Enrich via Anthropic Messages API (optional live provider)."""
    raise NotImplementedError(
        "Anthropic is an optional live provider and is not wired in this public repo. "
        "Use LLM_PROVIDER=mock (default) to run without API keys."
    )
