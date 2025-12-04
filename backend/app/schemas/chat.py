from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    content: str


class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class Citation(BaseModel):
    doc_id: int
    chunk_id: int
    score: float
    snippet: str
    metadata: Optional[dict] = None


class ChatResponse(BaseModel):
    message: MessageRead
    citations: List[Citation] = []
