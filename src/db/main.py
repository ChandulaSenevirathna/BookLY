from sqlmodel import create_engine, text, SQLModel
from sqlmodel.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import config
from src.books import models


engine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:       
       await conn.run_sync(SQLModel.metadata.create_all)
       

async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session