from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
)
from app.schemas.face_registration import RegisterFaceResponse
from app.services.employee import employee_service

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get(
    "/",
    response_model=list[EmployeeResponse],
)
def get_employees(
    db: Session = Depends(get_db),
):
    return employee_service.get_employees(db=db)


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return employee_service.get_employee_by_id(
        db=db,
        employee_id=employee_id,
    )


@router.post(
    "/",
    response_model=EmployeeResponse,
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return employee_service.create_employee(
        db=db,
        employee_data=employee,
    )


@router.post(
    "/{employee_id}/register-face",
    response_model=RegisterFaceResponse,
)
def register_face(
    employee_id: int,
    files: list[UploadFile] = File(..., description="Face images for each angle"),
    angles: str = Form(..., description="Comma-separated angles, e.g. front,left,right,up,down"),
    db: Session = Depends(get_db),
):
    angle_list = [a.strip() for a in angles.split(",")]
    return employee_service.register_face(
        db=db,
        employee_id=employee_id,
        files=files,
        angles=angle_list,
    )