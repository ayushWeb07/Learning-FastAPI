from pydantic import BaseModel, Field
from pydantic_extra_types.mime_types import StrEnum


class Status(StrEnum):
    placed = "placed"
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    shipped = "shipped"
    delivered = "delivered"

class ShipmentModel(BaseModel):
    id: int
    weight: float= Field(gt= 10.0)
    content: str= Field(min_length=4, max_length= 15)
    status: Status

class CreateShipmentDTO(BaseModel):
    weight: float = Field(gt=10.0)
    content: str = Field(min_length=4, max_length=15)
    status: Status

class UpdateShipmentDTO(BaseModel):
    weight: float = Field(gt=10.0)
    content: str = Field(min_length=4, max_length=15)
    status: Status