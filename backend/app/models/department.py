from typing import Optional

from sqlmodel import SQLModel, Field


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: int = Field(index=True, foreign_key="organization.id")
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="department.id")
