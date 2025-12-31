from fastapi import FastAPI

from app.api.driver import router as driver_router
from app.api.automobile import router as automobile_router
from app.api.trip import router as trip_router

app = FastAPI(title="Trucking API")

app.include_router(driver_router)
app.include_router(automobile_router)
app.include_router(trip_router)
