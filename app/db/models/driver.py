from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    personnel_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)

    trips = relationship("Trip", back_populates="driver")