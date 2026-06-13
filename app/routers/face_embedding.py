from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.face_embedding import (
    FaceEmbeddingCreate,
    FaceEmbeddingResponse,
    FaceEmbeddingMatch,
    RecognizeFaceRequest,
    RecognizeImageResponse,
)
from app.services.face_embedding import face_embedding_service

router = APIRouter(
    prefix="/face-embeddings",
    tags=["Face Embeddings"],
)


@router.get(
    "/",
    response_model=list[FaceEmbeddingResponse],
)
def get_embeddings(
    employee_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return face_embedding_service.get_embeddings(
        db=db,
        employee_id=employee_id,
    )


@router.get(
    "/active",
    response_model=list[FaceEmbeddingResponse],
)
def get_active_embeddings(
    employee_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return face_embedding_service.get_active_embeddings(
        db=db,
        employee_id=employee_id,
    )


@router.post(
    "/",
    response_model=FaceEmbeddingResponse,
)
def create_embedding(
    data: FaceEmbeddingCreate,
    db: Session = Depends(get_db),
):
    return face_embedding_service.create_embedding(
        db=db,
        data=data,
    )


@router.post(
    "/recognize",
    response_model=list[FaceEmbeddingMatch],
)
def recognize_face(
    data: RecognizeFaceRequest,
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    return face_embedding_service.find_similar(
        db=db,
        query_embedding=data.embedding,
        limit=limit,
    )


@router.patch(
    "/{embedding_id}/deactivate",
    response_model=FaceEmbeddingResponse,
)
def deactivate_embedding(
    embedding_id: int,
    db: Session = Depends(get_db),
):
    return face_embedding_service.deactivate_embedding(
        db=db,
        embedding_id=embedding_id,
    )


@router.post(
    "/recognize-image",
    response_model=RecognizeImageResponse,
)
def recognize_image(
    file: UploadFile = File(..., description="Face image to recognize"),
    db: Session = Depends(get_db),
):
    return face_embedding_service.recognize_image(
        db=db,
        file=file,
    )
