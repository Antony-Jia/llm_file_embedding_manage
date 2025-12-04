from typing import List

from fastapi import APIRouter

from app.schemas.org import DepartmentCreate, DepartmentRead, OrganizationCreate, OrganizationRead

router = APIRouter(prefix="/org", tags=["organization"])


@router.post("/organizations", response_model=OrganizationRead)
def create_organization(payload: OrganizationCreate) -> OrganizationRead:
    return OrganizationRead(id=1, name=payload.name, created_at=None)


@router.get("/organizations", response_model=List[OrganizationRead])
def list_organizations() -> List[OrganizationRead]:
    return []


@router.post("/departments", response_model=DepartmentRead)
def create_department(payload: DepartmentCreate) -> DepartmentRead:
    return DepartmentRead(id=1, name=payload.name, parent_id=payload.parent_id, org_id=1)


@router.get("/departments", response_model=List[DepartmentRead])
def list_departments() -> List[DepartmentRead]:
    return []
