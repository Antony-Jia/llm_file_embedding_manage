from typing import Optional

from sqlmodel import SQLModel, Field


class UserOrganization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    org_id: int = Field(foreign_key="organization.id")
    role: str = "member"
