from datetime import datetime

from pydantic import BaseModel


class FaceEmbeddingCreate(BaseModel):
    employee_id: int
    embedding: list[float]
    angle: str
    face_image_path: str | None = None
    confidence: float
    device_name: str | None = None


class FaceEmbeddingResponse(BaseModel):
    id: int
    employee_id: int
    angle: str
    face_image_path: str | None = None
    confidence: float
    is_active: bool
    device_name: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class FaceEmbeddingMatch(BaseModel):
    employee_id: int
    employee_code: str
    full_name: str
    distance: float
    angle: str
    face_image_path: str | None = None


class RecognizeImageResponse(BaseModel):
    employee_id: int | None = None
    employee_code: str | None = None
    full_name: str | None = None
    distance: float
    matched: bool


class RecognizeFaceRequest(BaseModel):
    embedding: list[float]
