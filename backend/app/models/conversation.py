from datetime import datetime
from typing import Optional

from sqlmodel import JSON, SQLModel, Field


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(index=True, foreign_key="organization.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    title: str
    scope_type: str
    scope_doc_ids: Optional[list] = Field(default=None, sa_column_kwargs={"type_": JSON})
    scope_metadata_filter: Optional[dict] = Field(default=None, sa_column_kwargs={"type_": JSON})
    llm_config_id: Optional[int] = Field(default=None, foreign_key="llmconfig.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
