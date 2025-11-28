from typing import List

from fastapi import APIRouter

router = APIRouter(prefix="/embeddings", tags=["embeddings"])


@router.post("/generate")
def generate_embeddings(texts: List[str]) -> dict:
    # Placeholder: return zeros to illustrate interface
    return {"embeddings": [[0.0 for _ in range(3)] for _ in texts]}
