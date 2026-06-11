from __future__ import annotations

from .models import EnrichedMetadata


class ValidationError(ValueError):
    pass


def validate(record: EnrichedMetadata) -> None:
    """Validate enriched metadata record. Raises ValidationError if invalid."""
    if not record.doi:
        raise ValidationError("DOI is required")
    if not record.title:
        raise ValidationError(f"Title is missing for DOI {record.doi!r}")
    if not record.ai_summary:
        raise ValidationError(f"AI summary is missing for DOI {record.doi!r}")
