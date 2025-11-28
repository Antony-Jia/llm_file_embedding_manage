from typing import Optional

from sqlmodel import SQLModel, Field


class UserDepartment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    dept_id: int = Field(foreign_key="department.id")
