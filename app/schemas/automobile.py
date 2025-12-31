from pydantic import BaseModel
from typing import Optional


class AutomobileBase(BaseModel):
    license_plate: str
    make: str
    capacity: float
    fuel_consumption: float


class AutomobileCreate(AutomobileBase):
    pass

class AutomobileUpdate(BaseModel):
    make: Optional[str] = None
    capacity: Optional[float] = None
    fuel_consumption: Optional[float] = None


class AutomobileOut(AutomobileBase):
    id: int

    class Config:
        from_attributes = True
