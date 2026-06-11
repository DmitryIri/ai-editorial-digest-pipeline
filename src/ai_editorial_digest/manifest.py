from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_dict(data: dict[str, Any]) -> str:
    """Compute SHA-256 of a canonical JSON-serialized dict."""
    canonical = json.dumps(data, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_manifest(records: list[dict[str, Any]], output_path: Path) -> dict[str, Any]:
    """Build a manifest with per-record checksums and a root checksum.

    Writes the manifest to output_path and returns it as a dict.
    """
    items = [{"doi": r.get("doi", "unknown"), "checksum": sha256_dict(r)} for r in records]
    manifest: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "items": items,
        "root_checksum": sha256_dict({"items": items}),
    }
    output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest
