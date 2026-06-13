from datetime import datetime, UTC
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.face_recognition_service import get_face_recognition_service
from app.core.config import FACES_DIR
from app.models.employee import Employee
from app.models.face_embedding import FaceEmbedding
from app.schemas.employee import EmployeeCreate
from app.schemas.face_registration import RegisterFaceResponse


ALLOWED_ANGLES = {"front", "left", "right", "up", "down"}


class EmployeeService:

    def get_employees(
        self,
        db: Session,
    ):
        statement = select(Employee)
        employees = db.scalars(
            statement
        ).all()
        return employees

    def get_employee_by_id(
        self,
        db: Session,
        employee_id: int,
    ):
        statement = select(Employee).where(
            Employee.id == employee_id
        )
        employee = db.scalars(
            statement
        ).first()

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )
        return employee

    def create_employee(
        self,
        db: Session,
        employee_data: EmployeeCreate
    ):

        employee = Employee(
            employee_code=employee_data.employee_code,
            full_name=employee_data.full_name,
            department=employee_data.department,
            position=employee_data.position,
            created_at=datetime.now(UTC),
        )

        db.add(employee)

        db.commit()

        db.refresh(employee)

        return employee

    def register_face(
        self,
        db: Session,
        employee_id: int,
        files: list[UploadFile],
        angles: list[str],
    ) -> RegisterFaceResponse:
        if len(files) != len(angles):
            raise HTTPException(
                status_code=400,
                detail="Number of files must match number of angles",
            )

        if not set(angles).issubset(ALLOWED_ANGLES):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid angles. Allowed: {ALLOWED_ANGLES}",
            )

        if len(angles) != len(set(angles)):
            raise HTTPException(
                status_code=400,
                detail="Duplicate angles not allowed",
            )

        employee = self.get_employee_by_id(db, employee_id)

        existing_angles = db.scalars(
            select(FaceEmbedding.angle).where(
                FaceEmbedding.employee_id == employee.id,
                FaceEmbedding.is_active == True,
            )
        ).all()

        for angle in angles:
            if angle in existing_angles:
                raise HTTPException(
                    status_code=400,
                    detail=f"Angle '{angle}' already registered for this employee",
                )

        employee_dir = FACES_DIR / employee.employee_code
        employee_dir.mkdir(parents=True, exist_ok=True)

        embeddings = []

        for file, angle in zip(files, angles):
            image_bytes = file.file.read()
            file.file.seek(0)

            extracted = get_face_recognition_service().extract_embedding(image_bytes)

            image_path = employee_dir / f"{angle}.jpg"
            image_path.write_bytes(image_bytes)

            face_embedding = FaceEmbedding(
                employee_id=employee.id,
                embedding=extracted.embedding,
                angle=angle,
                face_image_path=str(image_path),
                confidence=extracted.confidence,
            )

            db.add(face_embedding)
            embeddings.append(face_embedding)

        db.commit()

        for emb in embeddings:
            db.refresh(emb)

        return RegisterFaceResponse(
            employee_id=employee.id,
            employee_code=employee.employee_code,
            embeddings=embeddings,
        )


employee_service = EmployeeService()