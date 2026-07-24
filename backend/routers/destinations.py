from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..database import get_db
from ..schemas.destination import DestinationCreate, DestinationResponse, DestinationSearch
from ..services.destination_service import DestinationService
from ..models.destination import TravelInterest, BudgetLevel, TravelType

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=list[DestinationResponse])
async def list_destinations(db: AsyncSession = Depends(get_db)):
    service = DestinationService(db)
    return await service.get_all()


@router.get("/search", response_model=list[DestinationResponse])
async def search_destinations(
    travel_type: Optional[TravelType] = None,
    budget: Optional[BudgetLevel] = None,
    interest: Optional[TravelInterest] = None,
    query: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    service = DestinationService(db)
    params = DestinationSearch(travel_type=travel_type, budget=budget, interest=interest, query=query)
    return await service.search(params)


@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(destination_id: str, db: AsyncSession = Depends(get_db)):
    service = DestinationService(db)
    dest = await service.get_by_id(destination_id)
    if not dest:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Destination not found")
    return dest
