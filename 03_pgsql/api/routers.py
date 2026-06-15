from fastapi import HTTPException, status
from fastapi import APIRouter
from db.session import SessionDependency
from sqlmodel import select
from db.models import ShipmentModel
from dtos import GetShipmentDTO, CreateShipmentDTO, UpdateShipmentDTO

shipments_router= APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={}
)

# get all shipments
@shipments_router.get("/", status_code= status.HTTP_200_OK, response_model= list[GetShipmentDTO])
async def get_all_shipments(session: SessionDependency):
    result= await session.exec(select(ShipmentModel))
    shipments= result.all()
    return shipments

# get shipment by id
@shipments_router.get("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
async def get_shipment_by_id(shipment_id: int, session: SessionDependency):
    shipment= await session.get(ShipmentModel, shipment_id)

    if not shipment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

    return shipment

# create shipment
@shipments_router.post("/", status_code= status.HTTP_201_CREATED, response_model= GetShipmentDTO)
async def create_shipment(shipment: CreateShipmentDTO, session: SessionDependency):
    new_shipment = ShipmentModel(**shipment.model_dump())
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    if not new_shipment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create the shipment")

    return new_shipment

# update shipment
@shipments_router.patch("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
async def update_shipment(shipment_id: int, shipment: UpdateShipmentDTO, session: SessionDependency):
    existing_shipment = await session.get(ShipmentModel, shipment_id)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    existing_shipment.sqlmodel_update(shipment.model_dump(exclude_none= True))

    session.add(existing_shipment)
    await session.commit()
    await session.refresh(existing_shipment)

    return existing_shipment

# delete shipment
@shipments_router.delete("/{shipment_id}", status_code= status.HTTP_200_OK, response_model= dict[str, str])
async def delete_shipment(shipment_id: int, session: SessionDependency):
    existing_shipment = await session.get(ShipmentModel, shipment_id)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    await session.delete(existing_shipment)
    await session.commit()

    return {
        "status": "Successfully deleted the shipment",
    }