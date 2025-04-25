from app.database.db import Base, engine

# Import all models here so they are registered with SQLAlchemy
from app.models.survey import Survey

# Create tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine) 