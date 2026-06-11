from fastapi import FastAPI

from app.routers.employee import router as employee_router
from app.routers.face_embedding import router as face_embedding_router

app = FastAPI(
    title="Face Attendance"
)

app.include_router(employee_router)
app.include_router(face_embedding_router)


@app.get("/")
def root():
    return {
        "message": "Face Attendance API"
    }