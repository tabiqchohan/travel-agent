from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    id: str
    user_id: Optional[str] = None
    role: str
    content: str
    category: str = "general"
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageResponse]
    total: int
