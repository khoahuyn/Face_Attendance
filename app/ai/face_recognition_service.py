from dataclasses import dataclass
from functools import lru_cache

import cv2
import numpy as np
from fastapi import HTTPException
from insightface.app import FaceAnalysis


@dataclass
class ExtractedFace:
    embedding: list[float]
    confidence: float
    bbox: list[float]


class FaceRecognitionService:

    def __init__(self):
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
        )
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def extract_embedding(self, image_bytes: bytes) -> ExtractedFace:
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise HTTPException(
                status_code=400,
                detail="Cannot decode image",
            )

        faces = self.app.get(image)

        if not faces:
            raise HTTPException(
                status_code=400,
                detail="No face detected in image",
            )

        face = max(faces, key=lambda f: f.det_score)

        return ExtractedFace(
            embedding=face.embedding.tolist(),
            confidence=float(face.det_score),
            bbox=face.bbox.tolist(),
        )


@lru_cache
def get_face_recognition_service() -> FaceRecognitionService:
    return FaceRecognitionService()
