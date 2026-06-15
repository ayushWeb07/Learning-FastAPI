from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from api.services import ShipmentService
from db.session import get_session

SessionDependency= Annotated[AsyncSession, Depends(get_session)]

def get_service(session: SessionDependency) -> ShipmentService:
    return ShipmentService(session)

ServiceDependency= Annotated[ShipmentService, Depends(get_service)]