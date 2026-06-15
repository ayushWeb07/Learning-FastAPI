from datetime import datetime

from pydantic_extra_types.mime_types import StrEnum
from sqlmodel import Field, SQLModel

class ShipmentStatus(StrEnum):
    CREATED = 'CREATED'
    DELIVERED = 'DELIVERED'
    CANCELED = 'CANCELED'

class ShipmentModel(SQLModel, table=True):
    __tablename__ = 'shipments'
    
    id: int= Field(primary_key=True)
    content: str= Field(nullable=False, min_length= 5, max_length=100)
    weight: float= Field(nullable=False, default=1.0, gt=0.0, lt= 100.0)
    destination: str= Field(nullable=False, min_length= 5, max_length=100)
    status: ShipmentStatus= Field(nullable=False, default=ShipmentStatus.CREATED)
    delivery_date: datetime= Field(nullable=False, default=datetime.now())