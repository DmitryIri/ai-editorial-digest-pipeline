#!/usr/bin/env python3
"""Quickstart: enrich a list of synthetic DOIs and print the results."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_editorial_digest.pipeline import run_pipeline

SYNTHETIC_DOIS = [
    "10.9999/synthetic.2024.001",
    "10.9999/synthetic.2024.002",
]

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir)
        records = run_pipeline(SYNTHETIC_DOIS, output_dir=out_dir)
        manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))

    print(f"Enriched {len(records)} records:\n")
    for record in records:
        print(f"DOI:        {record['doi']}")
        print(f"Title:      {record['title']}")
        print(f"AI Summary: {record['ai_summary']}")
        print(f"AI Topics:  {', '.join(record['ai_topics'])}")
        print(f"Provider:   {record['enrichment_provider']}")
        print()

    print(f"Manifest root checksum: {manifest['root_checksum'][:24]}...")
    print(f"Records:                {manifest['record_count']}")
