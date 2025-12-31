from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.trip import TripCreate, TripOut
from app.crud.trip import create_trip, get_trips_by_driver

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/", response_model=TripOut)
async def create(data: TripCreate, session: AsyncSession = Depends(get_session)):
    return await create_trip(session, **data.model_dump())


@router.get("/driver/{driver_id}", response_model=list[TripOut])
async def get_by_driver(driver_id: int, session: AsyncSession = Depends(get_session)):
    return await get_trips_by_driver(session, driver_id)
