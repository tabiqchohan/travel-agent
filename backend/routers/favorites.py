from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.favorite import FavoriteCreate, FavoriteResponse
from ..services.favorite_service import FavoriteService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("", response_model=FavoriteResponse, status_code=201)
async def add_favorite(data: FavoriteCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = FavoriteService(db)
    return await service.add(current_user.id, data)


@router.delete("/{favorite_id}", status_code=204)
async def remove_favorite(favorite_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = FavoriteService(db)
    deleted = await service.remove(current_user.id, favorite_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Favorite not found")


@router.get("", response_model=list[FavoriteResponse])
async def list_favorites(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = FavoriteService(db)
    return await service.get_user_favorites(current_user.id)
