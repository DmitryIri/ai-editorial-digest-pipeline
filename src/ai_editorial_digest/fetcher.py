from __future__ import annotations

import json
import os
from pathlib import Path

from .models import RawMetadata

_FIXTURES_PATH = Path(__file__).parent.parent.parent / "fixtures" / "sample_dois.json"


def fetch_metadata(doi: str) -> RawMetadata:
    """Fetch bibliographic metadata for a DOI.

    METADATA_PROVIDER env var controls the backend:
      - 'mock' (default): returns synthetic fixture data — no network calls
      - 'crossref': Crossref REST API (optional live provider, not wired here)
    """
    provider = os.getenv("METADATA_PROVIDER", "mock")
    if provider == "mock":
        return _fetch_mock(doi)
    elif provider == "crossref":
        return _fetch_crossref(doi)
    else:
        raise ValueError(f"Unknown METADATA_PROVIDER: {provider!r}. Use 'mock' or 'crossref'.")


def _fetch_mock(doi: str) -> RawMetadata:
    """Return synthetic fixture data. Falls back to a minimal generated record if DOI not found."""
    if _FIXTURES_PATH.exists():
        fixtures = json.loads(_FIXTURES_PATH.read_text(encoding="utf-8"))
        for item in fixtures:
            if item.get("doi") == doi:
                return RawMetadata(**item)
    return RawMetadata(
        doi=doi,
        title=f"Synthetic paper: {doi}",
        abstract=(
            "This is a synthetic abstract for testing purposes. "
            "It describes a hypothetical study with fictional results."
        ),
        authors=["A. Author", "B. Coauthor"],
        year=2024,
        journal="Journal of Synthetic Research",
        keywords=["synthetic", "test", "mock"],
    )


def _fetch_crossref(doi: str) -> RawMetadata:
    """Query Crossref REST API (optional live provider)."""
    raise NotImplementedError(
        "Crossref is an optional live provider and is not wired in this public repo. "
        "Use METADATA_PROVIDER=mock (default) for demo and CI."
    )
