from fastapi import APIRouter

from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(tags=["auth"])


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    # Placeholder logic for demo purposes
    token = create_access_token(user_id=1, org_id=1)
    return TokenResponse(access_token=token)
