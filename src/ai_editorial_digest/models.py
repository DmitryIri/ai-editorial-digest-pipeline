from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class RawMetadata(BaseModel):
    doi: str
    title: str
    abstract: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    year: Optional[int] = None
    journal: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)


class EnrichedMetadata(BaseModel):
    doi: str
    title: str
    abstract: Optional[str] = None
    authors: list[str] = Field(default_factory=list)
    year: Optional[int] = None
    journal: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)
    ai_summary: Optional[str] = None
    ai_keywords: list[str] = Field(default_factory=list)
    ai_topics: list[str] = Field(default_factory=list)
    enrichment_provider: str = "mock"
