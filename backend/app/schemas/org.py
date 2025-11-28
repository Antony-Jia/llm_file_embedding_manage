from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    id: int
    name: str
    created_at: datetime


class DepartmentCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None


class DepartmentRead(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    org_id: int
