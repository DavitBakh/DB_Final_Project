from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Automobile(Base):
    __tablename__ = "automobiles"

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True, nullable=False) 
    make = Column(String)                       
    capacity = Column(Float)                    
    fuel_consumption = Column(Float)            

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    personnel_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)                          
    category = Column(String)                      

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    departure_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime)
    distance = Column(Float)
    origin = Column(String, nullable=False)
    destination = Column(String)
    
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    auto_id = Column(Integer, ForeignKey("automobiles.id"))
    
    driver = relationship("Driver", backref="trips")
    auto = relationship("Automobile", backref="trips")