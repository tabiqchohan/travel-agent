from typing import Optional
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.smart import SmartRequest, SmartResponse
from ..services.smart_service import SmartService
from ..services.chat_service import ChatService
from ..utils.security import get_optional_user
from ..models.user import User

router = APIRouter(prefix="/smart", tags=["Smart Assistant"])


@router.post("", response_model=SmartResponse)
async def smart_assistant(
    req: SmartRequest,
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    user: Optional[User] = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        user = await get_optional_user(token=token, db=db)

    service = SmartService(db)
    response = await service.process(req.user_input)

    chat_service = ChatService(db)
    if user:
        await chat_service.save_message(user.id, "user", req.user_input, response.category)
        await chat_service.save_message(user.id, "assistant", response.result, response.category)

    return response
