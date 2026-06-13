from datetime import datetime

from pydantic import BaseModel


class AttendanceCheckinResponse(BaseModel):
    success: bool
    message: str | None = None
    employee_id: int | None = None
    employee_code: str | None = None
    full_name: str | None = None
    check_in_time: datetime | None = None
    confidence: float | None = None
    distance: float | None = None

    model_config = {"from_attributes": True}


class AttendanceCheckoutResponse(BaseModel):
    success: bool
    message: str | None = None
    employee_id: int | None = None
    employee_code: str | None = None
    full_name: str | None = None
    check_in_time: datetime | None = None
    check_out_time: datetime | None = None
    confidence: float | None = None
    distance: float | None = None

    model_config = {"from_attributes": True}


class AttendanceLogResponse(BaseModel):
    id: int
    employee_id: int
    work_date: datetime
    check_in_time: datetime | None = None
    check_out_time: datetime | None = None
    camera_id: str | None = None
    confidence_score: float
    recognition_distance: float
    created_at: datetime

    model_config = {"from_attributes": True}
