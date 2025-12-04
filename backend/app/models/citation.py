from typing import Optional

from sqlmodel import JSON, SQLModel, Field


class Citation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(index=True, foreign_key="message.id")
    document_id: int = Field(index=True, foreign_key="document.id")
    chunk_id: int = Field(index=True, foreign_key="documentchunk.id")
    score: float
    snippet: str
    metadata: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})
