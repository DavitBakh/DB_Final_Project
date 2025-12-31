from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base
from sqlalchemy.orm import relationship

class Automobile(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True, nullable=False)
    make = Column(String)
    capacity = Column(Float)
    fuel_consumption = Column(Float)
    
    trips = relationship("Trip", back_populates="automobile")
