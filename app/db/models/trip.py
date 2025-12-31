from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from db.base import Base
from sqlalchemy.orm import relationship

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    departure_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    distance = Column(Float)
    origin = Column(String, nullable=False)
    destination = Column(String)
    status = Column(String, default="planned") #planned, in_progress, completed
    
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    auto_id = Column(Integer, ForeignKey("automobiles.id"))
    
    driver = relationship("Driver", back_populates="trips")
    automobile = relationship("Automobile", back_populates="trips")