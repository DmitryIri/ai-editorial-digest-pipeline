import pytest

from ai_editorial_digest.models import EnrichedMetadata
from ai_editorial_digest.validator import ValidationError, validate


def _valid_record(**kwargs) -> EnrichedMetadata:
    defaults = dict(doi="10.9999/test.001", title="Test Paper", ai_summary="A summary.")
    defaults.update(kwargs)
    return EnrichedMetadata(**defaults)


def test_validate_passes_for_valid_record():
    validate(_valid_record())


def test_validate_fails_missing_doi():
    with pytest.raises(ValidationError, match="DOI is required"):
        validate(_valid_record(doi=""))


def test_validate_fails_missing_title():
    with pytest.raises(ValidationError, match="Title is missing"):
        validate(_valid_record(title=""))


def test_validate_fails_missing_summary():
    with pytest.raises(ValidationError, match="AI summary is missing"):
        validate(_valid_record(ai_summary=None))
