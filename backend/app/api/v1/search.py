from fastapi import APIRouter

from app.schemas.search import SemanticSearchRequest, SemanticSearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/semantic", response_model=SemanticSearchResponse)
def semantic_search(payload: SemanticSearchRequest) -> SemanticSearchResponse:
    result = {
        "results": [
            {
                "doc_id": 1,
                "doc_title": "示例文档",
                "chunk_id": 1,
                "score": 0.9,
                "snippet": payload.query,
                "metadata": {"page": 1},
            }
        ],
        "total": 1,
    }
    return SemanticSearchResponse(**result)
