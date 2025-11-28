from typing import Optional

from sqlmodel import JSON, SQLModel, Field


class DocumentChunk(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(index=True, foreign_key="document.id")
    chunk_index: int
    text: str
    embedding: Optional[list] = Field(default=None, sa_column_kwargs={"type_": JSON})
    page_number: Optional[int] = None
    metadata: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})
