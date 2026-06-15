from fastapi import FastAPI
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference
from db import session
from api import routers

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await session.create_all_tables() # create tables when the server starts
    yield

app= FastAPI(lifespan= lifespan_handler)

# scalar docs
@app.get("/scalar", include_in_schema= False)
def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title= "Shipments API",
    )

# register the routers
app.include_router(routers.shipments_router)