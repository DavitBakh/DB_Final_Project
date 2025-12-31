from datetime import date
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.automobile import Automobile
from db.models.driver import Driver
from db.models.trip import Trip
from db.session import get_session
from schemas.trip import TripCreate, TripOut, TripUpdate
from crud.trip import create_trip, delete_trip, get_trip, get_trips, get_trips_by_driver, update_trip

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("/", response_model=TripOut)
async def create(data: TripCreate, session: AsyncSession = Depends(get_session)):
    return await create_trip(session, **data.model_dump())


@router.get("/driver/{driver_id}", response_model=list[TripOut])
async def get_by_driver(driver_id: int, session: AsyncSession = Depends(get_session)):
    return await get_trips_by_driver(session, driver_id)

@router.get("/{id}", response_model=TripOut)
async def api_get_trip(id: int, db: AsyncSession = Depends(get_session)):
    obj = await get_trip(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Trip not found")
    return obj

@router.get("/", response_model=list[TripOut])
async def api_list_trips(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    return await get_trips(db, skip, limit)

@router.get("/trips/filter")
async def filter_trips(
    min_distance: float,
    date_from: date,
    date_to: date,
    driver_id: int,
    db: AsyncSession = Depends(get_session),
):
    stmt = (
        select(Trip)
        .where(
            Trip.distance >= min_distance,
            Trip.departure_date >= date_from,
            Trip.departure_date <= date_to,
            Trip.driver_id == driver_id
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/trips/with-details")
async def trips_with_details(db: AsyncSession = Depends(get_session)):
    stmt = (
        select(
            Trip.id,
            Driver.name.label("driver"),
            Automobile.license_plate,
            Trip.distance
        )
        .join(Driver, Trip.driver_id == Driver.id)
        .join(Automobile, Trip.auto_id == Automobile.id)
    )

    result = await db.execute(stmt)
    return result.mappings().all()


@router.put("/{id}", response_model=TripOut)
async def api_update_trip(id: int, obj_in: TripUpdate, db: AsyncSession = Depends(get_session)):
    return await update_trip(db, id, obj_in)

@router.delete("/{id}")
async def api_delete_trip(id: int, db: AsyncSession = Depends(get_session)):
    await delete_trip(db, id)
    return {"ok": True}