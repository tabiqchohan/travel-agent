import json
from typing import Optional

from ..schemas.budget import BudgetEstimateRequest, BudgetEstimateResponse, CostBreakdown, CURRENCIES


class BudgetService:
    BASE_COSTS = {
        "bali": {"flight": 800, "hotel_budget": 25, "hotel_mid": 80, "hotel_luxury": 350, "food_daily": 15, "activities_daily": 30},
        "maldives": {"flight": 1200, "hotel_budget": 100, "hotel_mid": 300, "hotel_luxury": 800, "food_daily": 50, "activities_daily": 80},
        "seychelles": {"flight": 1500, "hotel_budget": 80, "hotel_mid": 200, "hotel_luxury": 600, "food_daily": 40, "activities_daily": 60},
        "vietnam": {"flight": 700, "hotel_budget": 15, "hotel_mid": 40, "hotel_luxury": 120, "food_daily": 8, "activities_daily": 20},
        "italy": {"flight": 600, "hotel_budget": 40, "hotel_mid": 120, "hotel_luxury": 350, "food_daily": 35, "activities_daily": 40},
        "france": {"flight": 500, "hotel_budget": 50, "hotel_mid": 150, "hotel_luxury": 400, "food_daily": 40, "activities_daily": 50},
        "nepal": {"flight": 900, "hotel_budget": 10, "hotel_mid": 30, "hotel_luxury": 100, "food_daily": 6, "activities_daily": 25},
        "costa rica": {"flight": 500, "hotel_budget": 20, "hotel_mid": 60, "hotel_luxury": 200, "food_daily": 12, "activities_daily": 35},
        "switzerland": {"flight": 700, "hotel_budget": 60, "hotel_mid": 180, "hotel_luxury": 500, "food_daily": 50, "activities_daily": 80},
        "thailand": {"flight": 600, "hotel_budget": 15, "hotel_mid": 50, "hotel_luxury": 200, "food_daily": 8, "activities_daily": 25},
        "mexico": {"flight": 400, "hotel_budget": 18, "hotel_mid": 55, "hotel_luxury": 180, "food_daily": 10, "activities_daily": 25},
        "japan": {"flight": 800, "hotel_budget": 35, "hotel_mid": 120, "hotel_luxury": 400, "food_daily": 30, "activities_daily": 40},
        "portugal": {"flight": 550, "hotel_budget": 25, "hotel_mid": 70, "hotel_luxury": 200, "food_daily": 18, "activities_daily": 25},
        "turkey": {"flight": 500, "hotel_budget": 15, "hotel_mid": 50, "hotel_luxury": 150, "food_daily": 10, "activities_daily": 20},
        "greece": {"flight": 600, "hotel_budget": 30, "hotel_mid": 90, "hotel_luxury": 250, "food_daily": 25, "activities_daily": 30},
    }

    HOTEL_CATEGORY_MAP = {
        "budget": "hotel_budget",
        "mid_range": "hotel_mid",
        "luxury": "hotel_luxury",
    }

    async def estimate(self, req: BudgetEstimateRequest) -> BudgetEstimateResponse:
        dest_key = req.destination.lower()
        costs = self.BASE_COSTS.get(dest_key, self.BASE_COSTS["thailand"])

        hotel_key = self.HOTEL_CATEGORY_MAP.get(req.hotel_category, "hotel_mid")

        total = 0.0
        breakdown = CostBreakdown()

        if req.include_flight and req.origin:
            breakdown.flight = costs["flight"] * req.travelers
            total += breakdown.flight

        if req.include_hotel:
            breakdown.hotel = costs[hotel_key] * req.duration_days
            total += breakdown.hotel

        if req.include_food:
            breakdown.food = costs["food_daily"] * req.duration_days * req.travelers
            total += breakdown.food

        if req.include_activities:
            breakdown.activities = costs["activities_daily"] * req.duration_days * req.travelers
            total += breakdown.activities

        breakdown.misc = total * 0.1
        total += breakdown.misc

        tips = [
            f"Best time to visit {req.destination.title()}: shoulder season for lower prices",
            "Book flights 3-4 months in advance for best rates",
            "Consider local transportation instead of taxis to save money",
            "Eat at local markets and street food stalls for authentic and affordable meals",
        ]

        symbol = CURRENCIES.get(req.currency, "$")

        if req.currency != "USD":
            rates = {"EUR": 0.92, "GBP": 0.79, "JPY": 149.5, "INR": 83.0, "THB": 35.5,
                     "VND": 25450, "IDR": 15700, "TRY": 30.5, "MXN": 17.2, "CHF": 0.88,
                     "NPR": 133.0, "CRC": 511.0, "MVR": 15.4, "SCR": 13.6}
            rate = rates.get(req.currency, 1.0)
            total *= rate

        return BudgetEstimateResponse(
            destination=req.destination,
            duration_days=req.duration_days,
            travelers=req.travelers,
            currency=req.currency,
            currency_symbol=symbol,
            total_estimated_cost=round(total, 2),
            breakdown=breakdown,
            tips=tips,
        )
