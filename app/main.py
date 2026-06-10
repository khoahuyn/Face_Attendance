from fastapi import FastAPI

from app.routers.employee import router as employee_router

app = FastAPI(
    title="Face Attendance"
)

app.include_router(employee_router)

@app.get("/")
def root():
    return {
        "message": "Face Attendance API"
    }