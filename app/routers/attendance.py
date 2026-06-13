from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.attendance import (
    AttendanceCheckinResponse,
    AttendanceCheckoutResponse,
    AttendanceLogResponse,
)
from app.services.attendance import attendance_service

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"],
)


@router.post(
    "/checkin",
    response_model=AttendanceCheckinResponse,
)
def checkin(
    file: UploadFile = File(...),
    camera_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return attendance_service.checkin(
        db=db,
        file=file,
        camera_id=camera_id,
    )


@router.post(
    "/checkout",
    response_model=AttendanceCheckoutResponse,
)
def checkout(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return attendance_service.checkout(
        db=db,
        file=file,
    )


@router.get(
    "/",
    response_model=list[AttendanceLogResponse],
)
def get_attendance_logs(
    employee_id: int | None = Query(default=None),
    from_date: str | None = Query(default=None, alias="from"),
    to_date: str | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
):
    return attendance_service.get_attendance_logs(
        db=db,
        employee_id=employee_id,
        from_date=from_date,
        to_date=to_date,
    )
