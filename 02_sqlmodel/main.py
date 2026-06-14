from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager

from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session, select

from db.session import create_all_tables, SessionDependency
from db.models import ShipmentModel
from dtos import GetShipmentDTO, CreateShipmentDTO, UpdateShipmentDTO

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_all_tables() # create tables when the server starts
    yield

app= FastAPI(lifespan= lifespan_handler)

# scalar docs
@app.get("/scalar", include_in_schema= False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "Shipments API",
    )

# get all shipments
@app.get("/shipments", status_code= status.HTTP_200_OK, response_model= list[GetShipmentDTO])
def get_all_shipments(session: SessionDependency):
    shipments= session.exec(select(ShipmentModel)).all()
    return shipments

# get shipment by id
@app.get("/shipments/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
def get_shipment_by_id(shipment_id: int, session: SessionDependency):
    shipment= session.get(ShipmentModel, shipment_id)

    if not shipment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

    return shipment

# create shipment
@app.post("/shipments", status_code= status.HTTP_201_CREATED, response_model= GetShipmentDTO)
def create_shipment(shipment: CreateShipmentDTO, session: SessionDependency):
    new_shipment = ShipmentModel(**shipment.model_dump())
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    if not new_shipment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create the shipment")

    return new_shipment

# update shipment
@app.patch("/shipments/{shipment_id}", status_code= status.HTTP_200_OK, response_model= GetShipmentDTO)
async def update_shipment(shipment_id: int, shipment: UpdateShipmentDTO, session: SessionDependency):
    existing_shipment = session.get(ShipmentModel, shipment_id)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    existing_shipment.sqlmodel_update(shipment.model_dump(exclude_none= True))

    session.add(existing_shipment)
    session.commit()
    session.refresh(existing_shipment)

    return existing_shipment

# delete shipment
@app.delete("/shipments/{shipment_id}", status_code= status.HTTP_200_OK, response_model= dict[str, str])
async def delete_shipment(shipment_id: int, session: SessionDependency):
    existing_shipment = session.get(ShipmentModel, shipment_id)

    if not existing_shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found")

    session.delete(existing_shipment)
    session.commit()

    return {
        "status": "Successfully deleted the shipment",
    }