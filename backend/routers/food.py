from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..database import get_db
from ..schemas.food import FoodCreate, FoodResponse, FoodSearch
from ..services.food_service import FoodService
from ..models.food import FoodCategory

router = APIRouter(prefix="/food", tags=["Food"])


@router.get("", response_model=list[FoodResponse])
async def search_food(
    destination: str,
    category: Optional[FoodCategory] = None,
    vegetarian: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    service = FoodService(db)
    params = FoodSearch(destination=destination, category=category, vegetarian=vegetarian)
    return await service.search(params)


@router.get("/by-destination/{destination_name}", response_model=list[FoodResponse])
async def get_food_by_destination(destination_name: str, db: AsyncSession = Depends(get_db)):
    service = FoodService(db)
    return await service.get_by_destination_name(destination_name)
