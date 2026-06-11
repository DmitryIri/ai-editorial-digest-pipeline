from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .enricher import enrich
from .fetcher import fetch_metadata
from .manifest import build_manifest
from .validator import validate


def run_pipeline(
    dois: list[str],
    output_dir: Path,
    manifest_path: Optional[Path] = None,
) -> list[dict]:
    """Run the full enrichment pipeline for a list of DOIs.

    Fetches metadata, enriches via LLM, validates, and writes per-record JSON files.
    Writes a manifest with SHA-256 checksums to manifest_path
    (defaults to output_dir/manifest.json).
    Returns all enriched records as a list of dicts.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []

    for doi in dois:
        raw = fetch_metadata(doi)
        enriched = enrich(raw)
        validate(enriched)
        record = enriched.model_dump()
        records.append(record)

        safe_name = doi.replace("/", "_").replace(".", "_")
        (output_dir / f"{safe_name}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    if manifest_path is None:
        manifest_path = output_dir / "manifest.json"
    build_manifest(records, manifest_path)

    return records
