import asyncio
import random
from datetime import datetime, timedelta

import httpx
from faker import Faker

API_URL = "http://127.0.0.1:8000"

fake = Faker()

DRIVERS_COUNT = 2000
AUTOS_COUNT = 1000
TRIPS_COUNT = 10000


async def create_drivers(client: httpx.AsyncClient):
    drivers = []

    for i in range(DRIVERS_COUNT):
        payload = {
            "personnel_number": f"D-{10000 + i}",
            "name": fake.name(),
            "category": random.choice(["B", "C", "CE"]),
        }

        resp = await client.post("/drivers/", json=payload)
        resp.raise_for_status()
        drivers.append(resp.json())

    print(f"Drivers created: {len(drivers)}")
    return drivers



async def create_automobiles(client: httpx.AsyncClient):
    autos = []

    for i in range(AUTOS_COUNT):
        payload = {
            "license_plate": f"AA{i:04d}BB",
            "make": random.choice(["Volvo", "Volkswagen", "Mercedes", "DAF", "BMW"]),
            "capacity": random.choice([5, 10, 20, 30]),
            "fuel_consumption": round(random.uniform(18, 35), 1),
        }

        resp = await client.post("/automobiles/", json=payload)
        resp.raise_for_status()
        autos.append(resp.json())

    print(f"Automobiles created: {len(autos)}")
    return autos

async def create_trips(client: httpx.AsyncClient, drivers: list[dict], autos: list[dict]):
    for _ in range(TRIPS_COUNT):
        driver = random.choice(drivers)
        auto = random.choice(autos)

        departure = datetime.utcnow() - timedelta(days=random.randint(0, 365))

        payload = {
            "driver_id": driver["id"],
            "auto_id": auto["id"],
            "origin": fake.city(),
            "destination": fake.city(),
            "departure_date": departure.isoformat(),
            "distance": round(random.uniform(20, 1200), 1),
        }

        resp = await client.post("/trips/", json=payload)
        resp.raise_for_status()

    print(f"Trips created: {TRIPS_COUNT}")



async def main():
    async with httpx.AsyncClient(base_url=API_URL, timeout=30.0) as client:
        drivers = await create_drivers(client)
        autos = await create_automobiles(client)
        await create_trips(client, drivers, autos)


if __name__ == "__main__":
    asyncio.run(main())
