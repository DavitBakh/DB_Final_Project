from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from db.models import Driver


async def create_driver(session: AsyncSession, personnel_number: str, name: str, category: str | None = None) -> Driver:
    driver = Driver(personnel_number=personnel_number, name=name, category=category)
    session.add(driver)
    await session.commit()
    await session.refresh(driver)
    return driver


async def get_driver_by_id(session: AsyncSession, driver_id: int) -> Driver | None:
    result = await session.execute(
        select(Driver)
        .where(Driver.id == driver_id))
    
    return result.scalar_one_or_none()


async def get_all_drivers(session: AsyncSession, skip: int = 0, limit: int = 100) -> list[Driver]:
    result = await session.execute(
        select(Driver).offset(skip).limit(limit))
    
    return result.scalars().all()


async def update_driver_name(session: AsyncSession, driver_id: int, new_name: str) -> bool:
    result = await session.execute(
        update(Driver)
        .where(Driver.id == driver_id)
        .values(name=new_name)
        .returning(Driver.id))
    
    await session.commit()
    return result.scalar() is not None


async def delete_driver(session: AsyncSession, driver_id: int) -> bool:
    result = await session.execute(
        delete(Driver)
        .where(Driver.id == driver_id)
        .returning(Driver.id))
    
    await session.commit()
    return result.scalar() is not None
