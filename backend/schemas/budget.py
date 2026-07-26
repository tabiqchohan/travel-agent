from typing import Optional
from pydantic import BaseModel, Field


CURRENCIES = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹",
    "THB": "฿", "VND": "₫", "IDR": "Rp", "TRY": "₺", "MXN": "Mex$",
    "CHF": "Fr", "NPR": "Rs", "CRC": "₡", "MVR": "Rf", "SCR": "₨",
}


class BudgetEstimateRequest(BaseModel):
    destination: str
    origin: Optional[str] = None
    duration_days: int = 7
    travelers: int = 1
    hotel_category: str = "mid_range"
    currency: str = "USD"
    include_flight: bool = True
    include_hotel: bool = True
    include_food: bool = True
    include_activities: bool = True


class CostBreakdown(BaseModel):
    flight: Optional[float] = None
    hotel: Optional[float] = None
    food: Optional[float] = None
    activities: Optional[float] = None
    misc: Optional[float] = None


class BudgetEstimateResponse(BaseModel):
    destination: str
    duration_days: int
    travelers: int
    currency: str = "USD"
    currency_symbol: str = "$"
    total_estimated_cost: float
    breakdown: CostBreakdown
    tips: list[str] = []
