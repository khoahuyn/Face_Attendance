from sqlalchemy import text

from app.core.database import engine
from app.models.base import Base
from app.models.employee import Employee
from app.models.face_embedding import FaceEmbedding

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(bind=engine)

print("Tables created")