from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import env_config

# create an engine
engine= create_async_engine(
    url= env_config.POSTGRES_CONNECTION_URI,
    echo= True,
)

# create the tables
async def create_all_tables():
    async with engine.begin() as conn:
        from .models import ShipmentModel
        await conn.run_sync(ShipmentModel.metadata.create_all)

async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session