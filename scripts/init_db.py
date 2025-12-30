import asyncio
import asyncpg
import os



async def init_db():
    password = os.getenv('POSTGRES_PASSWORD')
    if not password:
        raise RuntimeError("POSTGRES_PASSWORD environment variable is not set.")
    
    conn = await asyncpg.connect(
    user='postgres',
    password=password,
    host='localhost',
    port=5432,
    database='postgres'
)

    
    try:
        await conn.execute('CREATE DATABASE trucking_db OWNER postgres')
        print("База данных создана.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())