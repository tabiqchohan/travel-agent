from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.smart import SmartRequest, SmartResponse
from ..services.smart_service import SmartService

router = APIRouter(prefix="/smart", tags=["Smart Assistant"])


@router.post("", response_model=SmartResponse)
async def smart_assistant(req: SmartRequest, db: AsyncSession = Depends(get_db)):
    service = SmartService(db)
    return await service.process(req.user_input)
