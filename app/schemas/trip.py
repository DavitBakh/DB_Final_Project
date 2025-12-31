from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TripBase(BaseModel):
    driver_id: int
    auto_id: int
    origin: str
    destination: str
    departure_date: datetime
    distance: float

class TripCreate(TripBase):
    pass

class TripUpdate(BaseModel):
    return_date: Optional[datetime] = None
    distance: Optional[float] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    driver_id: Optional[int] = None
    auto_id: Optional[int] = None
    status: Optional[str] = None

class TripOut(TripCreate):
    id: int

    class Config:
        from_attributes = True
