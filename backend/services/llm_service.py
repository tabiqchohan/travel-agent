import json
import httpx
from typing import Optional

from ..config import settings


class GroqLLMService:
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 500) -> Optional[str]:
        if not self.available:
            return None

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    self.BASE_URL,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7,
                    },
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    print(f"Groq API error: {resp.status_code} {resp.text}")
                    return None
        except Exception as e:
            print(f"Groq request failed: {e}")
            return None

    async def recommend_destination(self, user_input: str, context: str) -> Optional[str]:
        system = """You are a professional travel assistant. Based on the user's preferences and available destinations, 
recommend the best destination(s). Be specific, enthusiastic, and provide reasons. 
Available destinations with details are provided in context. 
Keep response under 200 words."""
        prompt = f"User request: {user_input}\n\nAvailable destinations:\n{context}"
        return await self.generate(system, prompt)

    async def recommend_hotels(self, user_input: str, context: str) -> Optional[str]:
        system = """You are a hotel recommendation expert. Based on the user's request and available hotels,
recommend the best options. Categorize by budget. Keep response under 200 words."""
        prompt = f"User request: {user_input}\n\nAvailable hotels:\n{context}"
        return await self.generate(system, prompt)

    async def recommend_food(self, user_input: str, context: str) -> Optional[str]:
        system = """You are a local cuisine expert. Based on the user's request and available food options,
recommend dishes to try. Describe what makes each dish special. Keep response under 200 words."""
        prompt = f"User request: {user_input}\n\nAvailable food:\n{context}"
        return await self.generate(system, prompt)
