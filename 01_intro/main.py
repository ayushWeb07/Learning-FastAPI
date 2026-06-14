from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from data import shipments
from models import ShipmentModel, CreateShipmentDTO, UpdateShipmentDTO, UpdateShipmentStatusDTO

app= FastAPI()

# home route
@app.get("/", status_code= status.HTTP_200_OK)
async def get_home():
    return {"Hello": "World"}

# scalar docs
@app.get("/scalar", include_in_schema= False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "My First API",
    )

# get all shipments
@app.get("/shipments", status_code= status.HTTP_200_OK, response_model= list[ShipmentModel])
async def get_all_shipments():
    return shipments

# get shipment
@app.get("/shipments/{uid}", status_code= status.HTTP_200_OK, response_model= ShipmentModel)
async def get_shipment_by_id(uid: int):
    for s in shipments:
        if s["id"] == uid:
            return s

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

# create shipment
@app.post("/shipments", status_code= status.HTTP_201_CREATED, response_model= ShipmentModel)
async def create_shipment(shipment: CreateShipmentDTO):
    newId= len(shipments) + 1

    shipments.append({
        **shipment.model_dump(),
        "id": newId,
    })

    for s in shipments:
        if s["id"] == newId:
            return s

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create the shipment")

# update shipment
@app.put("/shipments/{uid}", status_code= status.HTTP_200_OK, response_model= ShipmentModel)
async def update_shipment(uid: int, shipment: UpdateShipmentDTO):
    for s in shipments:
        if s["id"] == uid:
            s["weight"]= shipment.weight
            s["content"]= shipment.content
            s["status"]= shipment.status

            return s

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update the shipment")

# update shipment status
@app.patch("/shipment-status/{uid}", status_code= status.HTTP_200_OK, response_model= UpdateShipmentStatusDTO)
async def update_shipment_status(uid: int, shipment: UpdateShipmentStatusDTO):
    for s in shipments:
        if s["id"] == uid:
            s["status"]= shipment.status
            return s

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update the shipment status")

# delete shipment
@app.delete("/shipments/{uid}", status_code= status.HTTP_200_OK, response_model= Dict[str, str])
async def delete_shipment(uid: int):
    for s in shipments:
        if s["id"] == uid:
            shipments.remove(s)

            return {
                "status": "Successfully deleted the shipment",
            }

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete the shipment")