from datetime import datetime, UTC

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.face_recognition_service import get_face_recognition_service
from app.core.config import FACE_RECOGNITION_THRESHOLD
from app.models.attendance import AttendanceLog
from app.models.employee import Employee
from app.models.face_embedding import FaceEmbedding


class AttendanceService:

    def _recognize_employee(self, db: Session, file: UploadFile):
        image_bytes = file.file.read()
        file.file.seek(0)

        extracted = get_face_recognition_service().extract_embedding(image_bytes)

        distance_expr = FaceEmbedding.embedding.cosine_distance(
            extracted.embedding
        ).label("distance")

        statement = (
            select(
                FaceEmbedding,
                Employee.employee_code,
                Employee.full_name,
                distance_expr,
            )
            .join(Employee, Employee.id == FaceEmbedding.employee_id)
            .where(FaceEmbedding.is_active.is_(True))
            .order_by("distance")
            .limit(1)
        )

        results = db.execute(statement).all()

        if not results:
            return None, None, None, None, None

        embedding, employee_code, full_name, distance = results[0]

        if distance > FACE_RECOGNITION_THRESHOLD:
            return None, None, None, None, None

        employee = db.get(Employee, embedding.employee_id)
        return employee, employee_code, full_name, extracted.confidence, distance

    def checkin(
        self,
        db: Session,
        file: UploadFile,
        camera_id: str | None = None,
    ):
        employee, employee_code, full_name, confidence, distance = (
            self._recognize_employee(db, file)
        )

        if employee is None:
            return {"success": False, "message": "Face not recognized"}

        now = datetime.now(UTC)
        work_date = now.date()

        existing = db.scalars(
            select(AttendanceLog).where(
                AttendanceLog.employee_id == employee.id,
                AttendanceLog.work_date == work_date,
            )
        ).first()

        if existing:
            return {"success": False, "message": "Already checked in today"}

        log = AttendanceLog(
            employee_id=employee.id,
            work_date=work_date,
            check_in_time=now,
            camera_id=camera_id,
            confidence_score=confidence,
            recognition_distance=distance,
        )

        db.add(log)
        db.commit()
        db.refresh(log)

        return {
            "success": True,
            "employee_id": employee.id,
            "employee_code": employee_code,
            "full_name": full_name,
            "check_in_time": log.check_in_time,
            "confidence": confidence,
            "distance": distance,
        }

    def checkout(
        self,
        db: Session,
        file: UploadFile,
    ):
        employee, employee_code, full_name, confidence, distance = (
            self._recognize_employee(db, file)
        )

        if employee is None:
            return {"success": False, "message": "Face not recognized"}

        now = datetime.now(UTC)
        work_date = now.date()

        log = db.scalars(
            select(AttendanceLog).where(
                AttendanceLog.employee_id == employee.id,
                AttendanceLog.work_date == work_date,
            )
        ).first()

        if not log:
            return {"success": False, "message": "No check-in found for today"}

        if log.check_out_time is not None:
            return {"success": False, "message": "Already checked out today"}

        log.check_out_time = now
        log.confidence_score = confidence
        log.recognition_distance = distance
        db.commit()
        db.refresh(log)

        return {
            "success": True,
            "employee_id": employee.id,
            "employee_code": employee_code,
            "full_name": full_name,
            "check_in_time": log.check_in_time,
            "check_out_time": log.check_out_time,
            "confidence": confidence,
            "distance": distance,
        }

    def get_attendance_logs(
        self,
        db: Session,
        employee_id: int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ):
        statement = select(AttendanceLog)

        if employee_id is not None:
            statement = statement.where(
                AttendanceLog.employee_id == employee_id,
            )
        if from_date is not None:
            statement = statement.where(
                AttendanceLog.work_date >= from_date,
            )
        if to_date is not None:
            statement = statement.where(
                AttendanceLog.work_date <= to_date,
            )

        statement = statement.order_by(AttendanceLog.work_date.desc())

        return db.scalars(statement).all()


attendance_service = AttendanceService()
