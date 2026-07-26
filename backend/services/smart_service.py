from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.destination import Destination
from ..schemas.smart import SmartRequest, SmartResponse
from ..config import settings
from .destination_service import DestinationService
from .hotel_service import HotelService
from .food_service import FoodService
from .llm_service import GroqLLMService


class SmartService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.dest_service = DestinationService(db)
        self.hotel_service = HotelService(db)
        self.food_service = FoodService(db)
        self.llm = GroqLLMService()

    DEST_KEYWORDS = ["travel", "where", "go", "destination", "trip", "vacation", "visit", "family", "budget", "interest", "holiday", "tour"]
    HOTEL_KEYWORDS = ["hotel", "stay", "accommodation", "place to stay", "lodging", "resort", "room", "hostel"]
    FOOD_KEYWORDS = ["food", "eat", "local food", "cuisine", "restaurant", "dishes", "drink", "dining", "lunch", "dinner", "breakfast", "street food"]
    PLAN_KEYWORDS = ["plan", "itinerary", "schedule", "day", "route", "trip plan", "travel plan", "multi-day"]

    async def process(self, user_input: str) -> SmartResponse:
        input_lower = user_input.lower()

        if any(kw in input_lower for kw in self.PLAN_KEYWORDS):
            result = await self._handle_destination_query(user_input, input_lower)
            return SmartResponse(result=result, category="trip_plan")
        elif any(kw in input_lower for kw in self.FOOD_KEYWORDS):
            result = await self._handle_food_query(user_input, input_lower)
            return SmartResponse(result=result, category="food")
        elif any(kw in input_lower for kw in self.HOTEL_KEYWORDS):
            result = await self._handle_hotel_query(user_input, input_lower)
            return SmartResponse(result=result, category="hotel")
        elif any(kw in input_lower for kw in self.DEST_KEYWORDS):
            result = await self._handle_destination_query(user_input, input_lower)
            return SmartResponse(result=result, category="destination")
        else:
            result = await self._handle_destination_query(user_input, input_lower)
            return SmartResponse(result=result, category="destination")

    async def _handle_destination_query(self, original: str, text: str) -> str:
        from ..schemas.destination import DestinationSearch
        from ..models.destination import TravelInterest, BudgetLevel, TravelType

        travel_type = None
        budget = None
        interest = None

        if any(w in text for w in ["family", "kids", "children"]):
            travel_type = "family"
        elif any(w in text for w in ["romantic", "honeymoon", "couple"]):
            travel_type = "romantic"
        elif any(w in text for w in ["solo", "alone", "single"]):
            travel_type = "solo"
        elif any(w in text for w in ["business", "work", "corporate"]):
            travel_type = "business"

        if any(w in text for w in ["low", "budget", "cheap", "affordable", "inexpensive"]):
            budget = "low"
        elif any(w in text for w in ["high", "luxury", "expensive", "premium"]):
            budget = "high"
        else:
            budget = "medium"

        if any(w in text for w in ["beach", "sea", "ocean", "coast"]):
            interest = "beach"
        elif any(w in text for w in ["culture", "history", "museum", "art", "heritage"]):
            interest = "culture"
        elif any(w in text for w in ["adventure", "hiking", "mountain", "trek", "extreme"]):
            interest = "adventure"
        elif any(w in text for w in ["food", "cuisine", "eat", "gourmet"]):
            interest = "food"

        search_params = DestinationSearch()
        if travel_type:
            try:
                search_params.travel_type = TravelType(travel_type)
            except ValueError:
                pass
        if budget:
            try:
                search_params.budget = BudgetLevel(budget)
            except ValueError:
                pass
        if interest:
            try:
                search_params.interest = TravelInterest(interest)
            except ValueError:
                pass

        results = await self.dest_service.search(search_params)

        if self.llm.available:
            context = "\n".join(
                f"{r.name}, {r.country}: {r.description[:150]} (Rating: {r.rating}, Budget: {r.budget_level.value})"
                for r in results[:5]
            ) if results else "No exact matches found. Suggest popular destinations."
            llm_result = await self.llm.recommend_destination(original, context)
            if llm_result:
                return llm_result

        if results:
            lines = [f"Based on your preferences, we recommend:"]
            for r in results[:3]:
                lines.append(f"\n**{r.name}, {r.country}**")
                lines.append(f"   {r.description[:100]}...")
                lines.append(f"   Rating: {r.rating}/5 | Budget: {r.budget_level.value}")
            return "\n".join(lines)
        else:
            return "No destinations found matching your criteria. Try different preferences!"

    async def _handle_hotel_query(self, original: str, text: str) -> str:
        destinations_list = [
            "bali", "maldives", "seychelles", "vietnam", "italy", "france",
            "nepal", "costa rica", "switzerland", "thailand", "mexico",
            "japan", "portugal", "turkey", "greece"
        ]
        found_dest = None
        for d in destinations_list:
            if d in text:
                found_dest = d
                break

        if not found_dest:
            return "Please specify a destination for hotel recommendations (e.g., 'hotels in Bali')."

        hotels = await self.hotel_service.get_by_destination_name(found_dest.title())

        if self.llm.available:
            context = "\n".join(
                f"{h.name} ({h.category.value}, ${h.price_per_night or 'N/A'}/night)"
                for h in hotels
            ) if hotels else "No hotels found."
            llm_result = await self.llm.recommend_hotels(original, context)
            if llm_result:
                return llm_result

        if not hotels:
            return f"No hotels found for {found_dest.title()}."

        lines = [f"**Hotel Recommendations for {found_dest.title()}:**\n"]
        for h in hotels:
            lines.append(f"**{h.name}**")
            lines.append(f"   Category: {h.category.value} | Price: ${h.price_per_night or 'N/A'}/night")
            lines.append("")
        return "\n".join(lines)

    async def _handle_food_query(self, original: str, text: str) -> str:
        destinations_list = [
            "bali", "maldives", "seychelles", "vietnam", "italy", "france",
            "nepal", "costa rica", "switzerland", "thailand", "mexico",
            "japan", "portugal", "turkey", "greece"
        ]
        found_dest = None
        for d in destinations_list:
            if d in text:
                found_dest = d
                break

        if not found_dest:
            return "Please specify a destination for food recommendations (e.g., 'food in Thailand')."

        foods = await self.food_service.get_by_destination_name(found_dest.title())

        if self.llm.available:
            context = "\n".join(
                f"{f.name} ({f.category.value if f.category else 'N/A'}, {f.price_range or ''})"
                for f in foods
            ) if foods else "No food items found."
            llm_result = await self.llm.recommend_food(original, context)
            if llm_result:
                return llm_result

        if not foods:
            return f"No food recommendations found for {found_dest.title()}."

        lines = [f"**Famous Food in {found_dest.title()}:**\n"]
        for f in foods:
            lines.append(f"• **{f.name}** - {f.price_range or ''} ({f.category.value if f.category else 'N/A'})")
        return "\n".join(lines)
