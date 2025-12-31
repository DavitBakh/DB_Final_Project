from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.driver import DriverCreate, DriverOut, DriverUpdate
from app.crud.driver import (
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
async def get_all(session: AsyncSession = Depends(get_session)):
    return await get_all_drivers(session)


@router.get("/{driver_id}", response_model=DriverOut)
async def get_by_id(driver_id: int, session: AsyncSession = Depends(get_session)):
    driver = await get_driver_by_id(session, driver_id)

    if not driver:
        raise HTTPException(404, "Driver not found")
    return driver


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
