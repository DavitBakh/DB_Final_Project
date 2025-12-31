from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.driver import Driver
from db.models.trip import Trip
from db.session import get_session
from schemas.driver import DriverCreate, DriverOut, DriverUpdate
from crud.driver import (
    create_driver,
    get_driver_by_id,
    get_all_drivers,
    update_driver_name,
    delete_driver,
)

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.post("/", response_model=DriverOut)
async def create(data: DriverCreate, session: AsyncSession = Depends(get_session)):
    return await create_driver(session, **data.model_dump())


@router.get("/", response_model=list[DriverOut])
async def get_all(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    return await get_all_drivers(session, skip, limit)


@router.get("/{driver_id}", response_model=DriverOut)
async def get_by_id(driver_id: int, session: AsyncSession = Depends(get_session)):
    driver = await get_driver_by_id(session, driver_id)

    if not driver:
        raise HTTPException(404, "Driver not found")
    return driver

@router.get("/stats/distance-by-driver")
async def distance_by_driver(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    stmt = (
        select(
            Driver.name,
            func.sum(Trip.distance).label("total_distance")
        )
        .join(Trip, Trip.driver_id == Driver.id)
        .group_by(Driver.name)
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(stmt)
    return result.mappings().all()



@router.put("/{driver_id}")
async def update(driver_id: int, data: DriverUpdate, session: AsyncSession = Depends(get_session)):
    updated = await update_driver_name(session, driver_id, data.name)

    if not updated:
        raise HTTPException(404, "Driver not found")
    return {"status": "updated"}


@router.delete("/{driver_id}")
async def delete(driver_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_driver(session, driver_id)

    if not deleted:
        raise HTTPException(404, "Driver not found")
    return {"status": "deleted"}
