import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

from base import Base
from session import engine

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST")
PORT = os.getenv("POSTGRES_PORT")


async def create_database():
    admin_url = (f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres")

    admin_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    async with admin_engine.connect() as conn:
        exists = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname=:name"),
            {"name": DB_NAME},
        )

        if not exists.scalar():
            await conn.execute(text(f'CREATE DATABASE "{DB_NAME}" OWNER "{USER}"'))
            print(f"База {DB_NAME} создана")
        else:
            print(f"База {DB_NAME} уже существует")

    await admin_engine.dispose()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы")


async def main():
    await create_database()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
