from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models import ShipmentModel
from dtos import CreateShipmentDTO, UpdateShipmentDTO


class ShipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_shipments(self):
        result = await self.session.exec(select(ShipmentModel))
        shipments = result.all()
        return shipments

    async def get_shipment_by_id(self, shipment_id: int):
        shipment = await self.session.get(ShipmentModel, shipment_id)
        return shipment

    async def create_shipment(self, shipment: CreateShipmentDTO):
        new_shipment = ShipmentModel(**shipment.model_dump())
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)

        return new_shipment

    async def update_shipment(self, shipment_id: int, shipment: UpdateShipmentDTO):
        existing_shipment = await self.session.get(ShipmentModel, shipment_id)

        if not existing_shipment:
            return None

        existing_shipment.sqlmodel_update(shipment.model_dump(exclude_none=True))

        self.session.add(existing_shipment)
        await self.session.commit()
        await self.session.refresh(existing_shipment)

        return existing_shipment

    async def delete_shipment(self, shipment_id: int):
        existing_shipment = await self.session.get(ShipmentModel, shipment_id)

        if not existing_shipment:
            return None

        await self.session.delete(existing_shipment)
        await self.session.commit()

        return existing_shipment
