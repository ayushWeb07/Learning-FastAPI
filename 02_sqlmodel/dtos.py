from datetime import datetime

from pydantic import BaseModel, Field
from db.models import ShipmentStatus

class GetShipmentDTO(BaseModel):
    id: int
    content: str
    weight: float
    destination: str
    status: ShipmentStatus
    delivery_date: datetime

class CreateShipmentDTO(BaseModel):
    content: str = Field(min_length=5, max_length=100)
    weight: float = Field(default=1.0, gt=0.0, lt=100.0)
    destination: str = Field(min_length=5, max_length=100)
    status: ShipmentStatus = Field(default=ShipmentStatus.CREATED)
    delivery_date: datetime = Field(default=datetime.now())

class UpdateShipmentDTO(BaseModel):
    content: str | None = Field(default= None, min_length=5, max_length=100)
    weight: float | None = Field(default=None, gt=0.0, lt=100.0)
    destination: str | None = Field(default=None, min_length=5, max_length=100)
    status: ShipmentStatus | None = Field(default=None)
    delivery_date: datetime | None = Field(default=None)