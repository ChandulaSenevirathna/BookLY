from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import config
from src.db import models
from sqlmodel import SQLModel

# Create async engine
engine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True
)

# Initialize database (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        
# test db connection       
async def test_db_connection():
    try:
        async with engine.connect() as conn:
            print("DB connection successful!")
    except Exception as e:
        print(f"DB connection failed: {e}")


# Session for async operations
async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session