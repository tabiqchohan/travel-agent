from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models.chat import ChatMessage
from ..schemas.chat import ChatMessageResponse


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_message(self, user_id: str | None, role: str, content: str, category: str = "general") -> ChatMessage:
        msg = ChatMessage(user_id=user_id, role=role, content=content, category=category)
        self.db.add(msg)
        await self.db.flush()
        return msg

    async def get_history(self, user_id: str, limit: int = 50) -> list[ChatMessageResponse]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = list(reversed(result.scalars().all()))
        return [ChatMessageResponse.model_validate(m) for m in messages]

    async def clear_history(self, user_id: str) -> None:
        await self.db.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self.db.flush()
