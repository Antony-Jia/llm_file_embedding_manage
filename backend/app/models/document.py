from datetime import datetime
from typing import List, Optional

from sqlmodel import JSON, SQLModel, Field


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(index=True, foreign_key="organization.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    title: str
    filename: str
    file_path: str
    file_type: str
    status: str = Field(default="uploaded")
    metadata: Optional[dict] = Field(sa_column_kwargs={"type_": JSON}, default=None)
    visibility_scope: str = Field(default="private")
    allowed_department_ids: Optional[List[int]] = Field(default=None, sa_column_kwargs={"type_": JSON})
    allowed_user_ids: Optional[List[int]] = Field(default=None, sa_column_kwargs={"type_": JSON})
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
