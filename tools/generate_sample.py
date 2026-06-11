#!/usr/bin/env python3
"""Generate sample output JSON for docs/demos. Uses mock provider only."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_editorial_digest.enricher import enrich
from ai_editorial_digest.fetcher import fetch_metadata
from ai_editorial_digest.manifest import build_manifest

DEMO_DOIS = [
    "10.9999/synthetic.2024.001",
    "10.9999/synthetic.2024.002",
    "10.9999/synthetic.2024.003",
]

output_dir = Path("examples")
output_dir.mkdir(exist_ok=True)

records = []
for doi in DEMO_DOIS:
    raw = fetch_metadata(doi)
    enriched = enrich(raw)
    records.append(enriched.model_dump())

sample_path = output_dir / "sample_output.json"
sample_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

manifest = build_manifest(records, output_dir / "sample_manifest.json")

print(f"Generated {len(records)} enriched records → {sample_path}")
print(f"Manifest root checksum: {manifest['root_checksum'][:24]}...")
