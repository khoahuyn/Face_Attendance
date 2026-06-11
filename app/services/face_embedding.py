from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.face_embedding import FaceEmbedding
from app.models.employee import Employee
from app.schemas.face_embedding import FaceEmbeddingCreate


class FaceEmbeddingService:

    def get_embeddings(
        self,
        db: Session,
        employee_id: int | None = None,
    ):
        statement = select(FaceEmbedding)
        if employee_id is not None:
            statement = statement.where(
                FaceEmbedding.employee_id == employee_id
            )
        return db.scalars(statement).all()

    def get_active_embeddings(
        self,
        db: Session,
        employee_id: int | None = None,
    ):
        statement = select(FaceEmbedding).where(
            FaceEmbedding.is_active.is_(True)
        )
        if employee_id is not None:
            statement = statement.where(
                FaceEmbedding.employee_id == employee_id
            )
        return db.scalars(statement).all()

    def create_embedding(
        self,
        db: Session,
        data: FaceEmbeddingCreate,
    ):
        employee = db.get(Employee, data.employee_id)
        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )

        embedding = FaceEmbedding(
            employee_id=data.employee_id,
            embedding=data.embedding,
            angle=data.angle,
            face_image_path=data.face_image_path,
            confidence=data.confidence,
            device_name=data.device_name,
        )

        db.add(embedding)
        db.commit()
        db.refresh(embedding)
        return embedding

    def find_similar(
        self,
        db: Session,
        query_embedding: list[float],
        threshold: float = 0.6,
        limit: int = 5,
    ):
        from pgvector.sqlalchemy import L2Distance

        statement = (
            select(
                FaceEmbedding,
                Employee.employee_code,
                Employee.full_name,
                L2Distance(FaceEmbedding.embedding, query_embedding).label("distance"),
            )
            .join(Employee, Employee.id == FaceEmbedding.employee_id)
            .where(FaceEmbedding.is_active.is_(True))
            .order_by("distance")
            .limit(limit)
        )

        results = db.execute(statement).all()

        matches = []
        for row in results:
            embedding, employee_code, full_name, distance = row
            if distance <= threshold:
                matches.append({
                    "employee_id": embedding.employee_id,
                    "employee_code": employee_code,
                    "full_name": full_name,
                    "distance": distance,
                    "angle": embedding.angle,
                    "face_image_path": embedding.face_image_path,
                })

        return matches

    def deactivate_embedding(
        self,
        db: Session,
        embedding_id: int,
    ):
        embedding = db.get(FaceEmbedding, embedding_id)
        if embedding is None:
            raise HTTPException(
                status_code=404,
                detail="Face embedding not found",
            )
        embedding.is_active = False
        db.commit()
        db.refresh(embedding)
        return embedding


face_embedding_service = FaceEmbeddingService()
