from pydantic import BaseModel

from app.schemas.face_embedding import FaceEmbeddingResponse


class RegisterFaceResponse(BaseModel):
    employee_id: int
    employee_code: str
    embeddings: list[FaceEmbeddingResponse]
