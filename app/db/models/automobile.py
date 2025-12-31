from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
from sqlalchemy.orm import relationship

class Automobile(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True, nullable=False, index=True)
    make = Column(String)
    capacity = Column(Float)
    fuel_consumption = Column(Float)
    year = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1)
    meta_data = Column(JSONB, nullable=True)
    
    trips = relationship("Trip", back_populates="automobile")
