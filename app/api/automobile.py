from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, desc, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.driver import update
from db.models.automobile import Automobile
from db.session import get_session
from schemas.automobile import AutomobileCreate, AutomobileOut, AutomobileUpdate
from crud.automobile import (
    create_automobile,
    get_automobile_by_plate,
    delete_automobile,
    update_automobile,
)

router = APIRouter(prefix="/automobiles", tags=["Automobiles"])

@router.get("/search")
async def search_automobiles(pattern: str, db: AsyncSession = Depends(get_session)):
    stmt = text("""
        SELECT *
        FROM automobiles
        WHERE meta_data::text ~* :pattern
    """
)
    result = await db.execute(stmt, {"pattern": pattern})
    return result.mappings().all()

@router.get("/ordered")
async def get_automobiles(
    sort_by: str = "id",
    order: str = "asc",
    db: AsyncSession = Depends(get_session),
):
    column = getattr(Automobile, sort_by, Automobile.id)

    stmt = select(Automobile)

    if order == "desc":
        stmt = stmt.order_by(desc(column))
    else:
        stmt = stmt.order_by(asc(column))

    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=AutomobileOut)
async def create(data: AutomobileCreate, session: AsyncSession = Depends(get_session)):
    return await create_automobile(session, **data.model_dump())

@router.get("/", response_model=list[AutomobileOut])
async def get_all(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Automobile))
    return result.scalars().all()

@router.get("/{plate}", response_model=AutomobileOut)
async def get_by_plate(plate: str, session: AsyncSession = Depends(get_session)):
    auto = await get_automobile_by_plate(session, plate)

    if not auto:
        raise HTTPException(404, "Automobile not found")
    return auto




@router.put("/{id}", response_model=AutomobileOut)
async def api_update_automobile(id: int, obj_in: AutomobileUpdate, db: AsyncSession = Depends(get_session)):
    return await update_automobile(db, id, obj_in)

@router.put("/automobiles/update-consumption")
async def update_consumption(
    capacity: float,
    make: str,
    db: AsyncSession = Depends(get_session),
):
    stmt = (
        update(Automobile)
        .where(
            Automobile.capacity > capacity,
            Automobile.make == make
        )
        .values(
            fuel_consumption=Automobile.fuel_consumption * 1.1
        )
    )

    await db.execute(stmt)
    await db.commit()

    return {"status": "updated"}



@router.delete("/{auto_id}")
async def delete(auto_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_automobile(session, auto_id)

    if not deleted:
        raise HTTPException(404, "Automobile not found")
    return {"status": "deleted"}
