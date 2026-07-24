from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional, List

from ..models.destination import Destination, TravelInterest, BudgetLevel, TravelType
from ..schemas.destination import DestinationCreate, DestinationResponse, DestinationSearch


class DestinationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, params: DestinationSearch) -> list[DestinationResponse]:
        query = select(Destination).where(Destination.is_active == True)

        if params.interest:
            query = query.where(Destination.interest == params.interest)
        if params.budget:
            query = query.where(Destination.budget_level == params.budget)
        if params.travel_type:
            query = query.where(Destination.travel_type == params.travel_type)
        if params.query:
            query = query.where(
                or_(
                    Destination.name.ilike(f"%{params.query}%"),
                    Destination.country.ilike(f"%{params.query}%"),
                    Destination.description.ilike(f"%{params.query}%"),
                )
            )

        query = query.order_by(Destination.rating.desc())
        result = await self.db.execute(query)
        destinations = result.scalars().all()
        return [DestinationResponse.model_validate(d) for d in destinations]

    async def get_by_id(self, dest_id: str) -> Optional[DestinationResponse]:
        result = await self.db.execute(select(Destination).where(Destination.id == dest_id))
        dest = result.scalar_one_or_none()
        return DestinationResponse.model_validate(dest) if dest else None

    async def create(self, data: DestinationCreate) -> DestinationResponse:
        dest = Destination(**data.model_dump())
        self.db.add(dest)
        await self.db.flush()
        return DestinationResponse.model_validate(dest)

    async def get_all(self) -> list[DestinationResponse]:
        result = await self.db.execute(
            select(Destination).where(Destination.is_active == True).order_by(Destination.rating.desc())
        )
        return [DestinationResponse.model_validate(d) for d in result.scalars().all()]
