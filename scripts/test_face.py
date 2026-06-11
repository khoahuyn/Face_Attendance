from pathlib import Path

from app.ai.face_recognition_service import get_face_recognition_service

image_path = Path(__file__).parent.parent / "test.jpg"
image_bytes = image_path.read_bytes()

service = get_face_recognition_service()
result = service.extract_embedding(image_bytes)

print(f"Embedding length: {len(result.embedding)}")
print(f"Confidence: {result.confidence:.4f}")
print(f"BBox: {result.bbox}")
