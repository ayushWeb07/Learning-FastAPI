from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from data import shipments
from models import ShipmentModel, CreateShipmentDTO, UpdateShipmentDTO

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
@app.get("/shipments", status_code= status.HTTP_200_OK)
async def get_all_shipments() -> list[ShipmentModel]:
    return shipments

# get shipment
@app.get("/shipments/{uid}", status_code= status.HTTP_200_OK)
async def get_shipment_by_id(uid: int) -> ShipmentModel:
    for s in shipments:
        if s["id"] == uid:
            return s

    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

# create shipment
@app.post("/shipments", status_code= status.HTTP_201_CREATED)
async def create_shipment(shipment: CreateShipmentDTO) -> ShipmentModel:
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
@app.put("/shipments/{uid}", status_code= status.HTTP_200_OK)
async def update_shipment(uid: int, shipment: UpdateShipmentDTO) -> ShipmentModel:
    for s in shipments:
        if s["id"] == uid:
            s["weight"]= shipment.weight
            s["content"]= shipment.content
            s["status"]= shipment.status

    for s in shipments:
        if s["id"] == uid:
            return s

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update the shipment")

# delete shipment
@app.delete("/shipments/{uid}", status_code= status.HTTP_200_OK)
async def delete_shipment(uid: int) -> Dict[str, str]:
    for s in shipments:
        if s["id"] == uid:
            shipments.remove(s)

            return {
                "status": "Successfully deleted the shipment",
            }

    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete the shipment")