from app.core.database import engine

from app.models.base import Base

from app.models.employee import Employee


Base.metadata.create_all(bind=engine)

print("Tables created")