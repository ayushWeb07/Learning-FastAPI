from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from config import env_config

# create an engine
engine= create_async_engine(
    url= env_config.POSTGRES_CONNECTION_URI,
    echo= True,
    connect_args= {
        "check_same_thread": False
    }
)

# create the tables
async def create_all_tables():
    async with engine.begin() as conn:
        from .models import ShipmentModel
        await conn.run_sync(ShipmentModel.metadata.create_all)

async def get_session():
    async_session= sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session

SessionDependency= Annotated[AsyncSession, Depends(get_session)]