from typing import List

from fastapi import APIRouter

from app.schemas.config import EmbeddingConfigCreate, LLMConfigCreate

router = APIRouter(prefix="/config", tags=["config"])


@router.post("/embedding", response_model=EmbeddingConfigCreate)
def create_embedding_config(payload: EmbeddingConfigCreate) -> EmbeddingConfigCreate:
    return payload


@router.get("/embedding", response_model=List[EmbeddingConfigCreate])
def list_embedding_configs() -> List[EmbeddingConfigCreate]:
    return []


@router.post("/llm", response_model=LLMConfigCreate)
def create_llm_config(payload: LLMConfigCreate) -> LLMConfigCreate:
    return payload


@router.get("/llm", response_model=List[LLMConfigCreate])
def list_llm_configs() -> List[LLMConfigCreate]:
    return []
