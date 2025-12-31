from pydantic import BaseModel


class AutomobileBase(BaseModel):
    license_plate: str
    make: str
    capacity: float
    fuel_consumption: float


class AutomobileCreate(AutomobileBase):
    pass


class AutomobileOut(AutomobileBase):
    id: int

    class Config:
        from_attributes = True
