from datetime import datetime
from pydantic import BaseModel


class TripCreate(BaseModel):
    driver_id: int
    auto_id: int
    origin: str
    destination: str
    departure_date: datetime
    distance: float


class TripOut(TripCreate):
    id: int

    class Config:
        from_attributes = True
