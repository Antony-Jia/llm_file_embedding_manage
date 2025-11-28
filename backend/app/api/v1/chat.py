from typing import List

from fastapi import APIRouter

from app.schemas.chat import ChatResponse, MessageCreate, MessageRead

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageRead])
def list_messages(conversation_id: int) -> List[MessageRead]:
    return []


@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
def send_message(conversation_id: int, payload: MessageCreate) -> ChatResponse:
    message = MessageRead(id=1, role="assistant", content=f"Echo: {payload.content}", created_at=None)
    return ChatResponse(message=message, citations=[])
