from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from schemas.automobile import AutomobileCreate, AutomobileOut, AutomobileUpdate
from crud.automobile import (
    create_automobile,
    get_automobile_by_plate,
    delete_automobile,
    update_automobile,
)

router = APIRouter(prefix="/automobiles", tags=["Automobiles"])


@router.post("/", response_model=AutomobileOut)
async def create(data: AutomobileCreate, session: AsyncSession = Depends(get_session)):
    return await create_automobile(session, **data.model_dump())


@router.get("/{plate}", response_model=AutomobileOut)
async def get_by_plate(plate: str, session: AsyncSession = Depends(get_session)):
    auto = await get_automobile_by_plate(session, plate)

    if not auto:
        raise HTTPException(404, "Automobile not found")
    return auto

@router.put("/{id}", response_model=AutomobileOut)
async def api_update_automobile(id: int, obj_in: AutomobileUpdate, db: AsyncSession = Depends(get_session)):
    return await update_automobile(db, id, obj_in)


@router.delete("/{auto_id}")
async def delete(auto_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_automobile(session, auto_id)

    if not deleted:
        raise HTTPException(404, "Automobile not found")
    return {"status": "deleted"}
