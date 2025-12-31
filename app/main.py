from fastapi import FastAPI

from api.driver import router as driver_router
from api.automobile import router as automobile_router
from api.trip import router as trip_router

app = FastAPI(title="Trucking API")

app.include_router(driver_router)
app.include_router(automobile_router)
app.include_router(trip_router)
