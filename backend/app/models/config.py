from typing import Optional

from sqlmodel import JSON, SQLModel, Field


class EmbeddingConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    provider: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str
    chunk_size: int = 1000
    chunk_overlap: int = 200
    settings: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})


class LLMConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str
    timeout: int = 60
    max_tokens: int = 1024
    settings: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})
