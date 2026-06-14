from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app= FastAPI()

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

@app.get("/shipment", status_code= status.HTTP_200_OK)
async def get_shipments(id: int | None= None):
    return {"id": "not provided" if id is None else id, "status": "pending"}

@app.get("/shipment/{id}", status_code= status.HTTP_200_OK)
async def get_shipment_by_id(id: int) -> dict[str, Any]:

    if id >= 100:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Shipment not found")

    return {
        "id": id,
        "status": "delivered",
        "date": datetime.now(),
    }