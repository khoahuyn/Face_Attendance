from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    department: str | None = None
    position: str | None = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    department: str | None = None
    position: str | None = None
    status: str

    model_config = {
        "from_attributes": True
    }   