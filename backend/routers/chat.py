from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.chat import ChatHistoryResponse
from ..services.chat_service import ChatService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    messages = await service.get_history(current_user.id, limit)
    return ChatHistoryResponse(messages=messages, total=len(messages))


@router.delete("/history")
async def clear_chat_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    await service.clear_history(current_user.id)
    return {"message": "Chat history cleared"}
