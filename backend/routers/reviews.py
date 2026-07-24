from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.review import ReviewCreate, ReviewResponse
from ..services.review_service import ReviewService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("", response_model=ReviewResponse, status_code=201)
async def create_review(data: ReviewCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.create(current_user.id, data)


@router.get("/destination/{destination_id}", response_model=list[ReviewResponse])
async def get_destination_reviews(destination_id: str, db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.get_by_destination(destination_id)


@router.get("/my", response_model=list[ReviewResponse])
async def get_my_reviews(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ReviewService(db)
    return await service.get_by_user(current_user.id)
