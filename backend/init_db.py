# init_db.py
import asyncio
from app.db.database import engine, Base
from app.core.config import settings 

async def create_tables():
    async with engine.begin() as conn:
        # For new DB, drop all first if you want a clean slate (optional)
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (if they didn't exist).")

if __name__ == "__main__":
    # Ensure DATABASE_URL is set in your environment or .env file
    # Example: DATABASE_URL=postgresql+asyncpg://user:pass@host/db
    if not settings.DATABASE_URL:
        print("Error: DATABASE_URL not set. Please check your .env file or environment variables.")
    else:
        asyncio.run(create_tables())