from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Trip


async def create_trip(session: AsyncSession, driver_id: int, auto_id: int, origin: str, destination: str, departure_date: datetime, distance: float) -> Trip:
    trip = Trip(driver_id=driver_id, auto_id=auto_id, origin=origin, destination=destination, departure_date=departure_date, distance=distance)
    session.add(trip)
    await session.commit()
    await session.refresh(trip)
    return trip


async def get_trips_by_driver(session: AsyncSession, driver_id: int) -> list[Trip]:
    result = await session.execute(
        select(Trip).where(Trip.driver_id == driver_id))

    return result.scalars().all()
