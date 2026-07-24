from pydantic import BaseModel


class SmartRequest(BaseModel):
    user_input: str


class SmartResponse(BaseModel):
    result: str
    category: str = "general"
