from pydantic import BaseModel


class DriverBase(BaseModel):
    personnel_number: str
    name: str
    category: str | None = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: str


class DriverOut(DriverBase):
    id: int

    class Config:
        from_attributes = True
