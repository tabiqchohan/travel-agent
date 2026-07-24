from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..database import get_db
from ..schemas.hotel import HotelCreate, HotelResponse, HotelSearch
from ..services.hotel_service import HotelService
from ..models.hotel import HotelCategory

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=list[HotelResponse])
async def search_hotels(
    destination: str,
    category: Optional[HotelCategory] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
):
    service = HotelService(db)
    params = HotelSearch(destination=destination, category=category, max_price=max_price)
    return await service.search(params)


@router.get("/by-destination/{destination_name}", response_model=list[HotelResponse])
async def get_hotels_by_destination(destination_name: str, db: AsyncSession = Depends(get_db)):
    service = HotelService(db)
    return await service.get_by_destination_name(destination_name)
