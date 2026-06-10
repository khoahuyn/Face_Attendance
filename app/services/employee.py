from datetime import datetime, UTC

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from fastapi import HTTPException


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


employee_service = EmployeeService()