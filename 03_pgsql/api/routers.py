from fastapi import HTTPException, status
from fastapi import APIRouter

from api.services import ShipmentService
from db.session import SessionDependency
from sqlmodel import select
from db.models import ShipmentModel
from dependencies import ServiceDependency
from dtos import GetShipmentDTO, CreateShipmentDTO, UpdateShipmentDTO

shipments_router= APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={}
)

# get all shipments
@shipments_router.get("/", status_code= status.HTTP_200_OK, response_model= list[GetShipmentDTO])
async def get_all_shipments(service: ServiceDependency):
    shipments= await service.get_all_shipments()
    return shipments

# get shipment by id
@shipments_router.get("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
async def get_shipment_by_id(shipment_id: int, service: ServiceDependency):
    shipment= await service.get_shipment_by_id(shipment_id)

    if not shipment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

    return shipment

# create shipment
@shipments_router.post("/", status_code= status.HTTP_201_CREATED, response_model= GetShipmentDTO)
async def create_shipment(shipment: CreateShipmentDTO, service: ServiceDependency):
    new_shipment= await service.create_shipment(shipment)

    if not new_shipment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create the shipment")

    return new_shipment

# update shipment
@shipments_router.patch("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
async def update_shipment(shipment_id: int, shipment: UpdateShipmentDTO, service: ServiceDependency):
    existing_shipment= await service.update_shipment(shipment_id, shipment)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    return existing_shipment

# delete shipment
@shipments_router.delete("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= dict[str, str])
async def delete_shipment(shipment_id: int, service: ServiceDependency):
    existing_shipment = await service.delete_shipment(shipment_id)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    return {
        "status": "Successfully deleted the shipment",
    }