from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from db.models import Trip


async def create_trip(session: AsyncSession, driver_id: int, auto_id: int, origin: str, destination: str, departure_date: datetime, distance: float) -> Trip:
    trip = Trip(driver_id=driver_id, auto_id=auto_id, origin=origin, destination=destination, departure_date=departure_date, distance=distance)
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip

async def get_trip(db: AsyncSession, id: int):
    result = await db.execute(select(Trip).where(Trip.id == id))
    return result.scalar_one_or_none()

async def get_trips(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Trip).offset(skip).limit(limit))
    return result.scalars().all()

async def update_trip(db: AsyncSession, id: int, obj_in):
    await db.execute(update(Trip).where(Trip.id == id).values(**obj_in.dict(exclude_unset=True)))
    await db.commit()
    return await get_trip(db, id)

async def get_trips_by_driver(session: AsyncSession, driver_id: int, skip: int = 0, limit: int = 100) -> list[Trip]:
    result = await session.execute(
        select(Trip).where(Trip.driver_id == driver_id).offset(skip).limit(limit))

    return result.scalars().all()

async def delete_trip(db: AsyncSession, id: int):
    await db.execute(delete(Trip).where(Trip.id == id))
    await db.commit()
    return True

