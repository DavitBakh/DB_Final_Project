from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from db.models import Automobile


async def create_automobile(session: AsyncSession, license_plate: str, make: str, capacity: float, fuel_consumption: float, meta_data: dict | None = None) -> Automobile:
    auto = Automobile(license_plate=license_plate, make=make, capacity=capacity, fuel_consumption=fuel_consumption, meta_data=meta_data)
    session.add(auto)
    await session.commit()
    await session.refresh(auto)
    return auto


async def get_automobile_by_plate(session: AsyncSession, plate: str) -> Automobile | None:
    result = await session.execute(
        select(Automobile)
        .where(Automobile.license_plate == plate))
        
    return result.scalar_one_or_none()

async def get_automobile(db: AsyncSession, id: int):
    result = await db.execute(select(Automobile).where(Automobile.id == id))
    return result.scalar_one_or_none()

async def update_automobile(db: AsyncSession, id: int, obj_in):
    await db.execute(update(Automobile).where(Automobile.id == id).values(**obj_in.dict(exclude_unset=True)))
    await db.commit()
    return await get_automobile(db, id)


async def delete_automobile(session: AsyncSession, auto_id: int) -> bool:
    result = await session.execute(
        delete(Automobile)
        .where(Automobile.id == auto_id)
        .returning(Automobile.id)
    )

    await session.commit()
    return result.scalar() is not None
