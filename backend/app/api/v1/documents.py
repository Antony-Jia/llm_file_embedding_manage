from typing import List

from fastapi import APIRouter, UploadFile

from app.schemas.document import DocumentRead, DocumentUploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
def upload_document(file: UploadFile) -> DocumentUploadResponse:
    return DocumentUploadResponse(id=1, title=file.filename, filename=file.filename, status="uploaded")


@router.get("/", response_model=List[DocumentRead])
def list_documents() -> List[DocumentRead]:
    return []
