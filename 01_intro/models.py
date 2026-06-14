from pydantic import BaseModel

class ShipmentModel(BaseModel):
    id: int
    weight: float
    content: str
    status: str

class CreateShipmentDTO(BaseModel):
    weight: float
    content: str
    status: str

class UpdateShipmentDTO(BaseModel):
    weight: float
    content: str
    status: str