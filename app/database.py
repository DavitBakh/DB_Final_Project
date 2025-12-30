from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

password = os.getenv('POSTGRES_PASSWORD')
if not password:
    raise RuntimeError("POSTGRES_PASSWORD environment variable is not set.")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost/trucking_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()