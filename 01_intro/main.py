from datetime import datetime
from typing import Any

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app= FastAPI()

@app.get("/")
async def get_home():
    return {"Hello": "World"}

# scalar docs
@app.get("/scalar", include_in_schema= False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "My First API",
    )

@app.get("/shipment")
async def get_shipment():
    return {"id": "123", "status": "delivered"}

@app.get("/shipment/{id}")
async def get_shipment(id: int) -> dict[str, Any]:
    return {
        "id": id,
        "status": "delivered",
        "date": datetime.now(),
    }