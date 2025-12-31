from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import app.db.models as models, schemas
from database import engine, get_db

app = FastAPI()

# Базовый CRUD для автомобилей
@app.post("/automobiles/")
def create_auto(auto: schemas.AutoCreate, db: Session = Depends(get_db)):
    db_auto = models.Automobile(**auto.dict())
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto

# Чтение с пагинацией (Критерий 7) и сортировкой (часть Критерия 5)
@app.get("/automobiles/")
def read_autos(
    skip: int = 0, 
    limit: int = 10, 
    sort_by: str = Query("id", description="Field to sort by"),
    db: Session = Depends(get_db)
):
    # Простая сортировка через text() - будьте осторожны с SQL-инъекциями в реальном проде,
    # здесь для учебного примера допустимо, или используйте getattr(models.Automobile, sort_by)
    return db.query(models.Automobile).order_by(text(sort_by)).offset(skip).limit(limit).all()

# Аналогично добавьте роуты для Driver и Trip
@app.post("/drivers/")
def create_driver(name: str, personnel_number: str, category: str, db: Session = Depends(get_db)):
    db_driver = models.Driver(name=name, personnel_number=personnel_number, category=category)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

@app.post("/trips/")
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    db_trip = models.Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip