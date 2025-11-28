from typing import Optional

from pydantic import BaseModel


class EmbeddingConfigCreate(BaseModel):
    name: str
    provider: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str
    chunk_size: int = 1000
    chunk_overlap: int = 200


class LLMConfigCreate(BaseModel):
    name: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str
    timeout: int = 60
    max_tokens: int = 1024
