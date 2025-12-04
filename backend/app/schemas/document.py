from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    id: int
    title: str
    filename: str
    status: str


class DocumentRead(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    status: str
    metadata: Optional[dict]
    visibility_scope: str
    allowed_department_ids: Optional[List[int]]
    allowed_user_ids: Optional[List[int]]
    created_at: datetime
    updated_at: datetime
