from typing import List, Optional

from pydantic import BaseModel


class SearchFilters(BaseModel):
    doc_ids: Optional[List[int]] = None
    project: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[dict] = None
    created_from: Optional[str] = None
    created_to: Optional[str] = None


class SemanticSearchRequest(BaseModel):
    query: str
    top_k: int = 10
    filters: Optional[SearchFilters] = None


class SemanticSearchResult(BaseModel):
    doc_id: int
    doc_title: str
    chunk_id: int
    score: float
    snippet: str
    metadata: Optional[dict] = None


class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult]
    total: int
