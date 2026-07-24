#!/usr/bin/env python3
"""
Professional Travel Agent Web API

This is a FastAPI web application version of the travel agent that can be run with Uvicorn.
It maintains the same tool system but exposes endpoints for web access.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


# Global tool registry
tools = {}


def tool(func):
    """
    Decorator to register functions in the global tools dictionary.
    Uses the function name as the tool name.
    """
    tools[func.__name__] = func
    return func


@tool
def destination_finder(travel_type: str, budget: str, interest: str):
    """
    Find travel destinations based on user preferences.

    Args:
        travel_type: Type of travel (e.g., "family", "romantic", "solo", "business")
        budget: Budget level (e.g., "low", "medium", "high")
        interest: Travel interests (e.g., "beach", "culture", "adventure", "food")

    Returns:
        Structured string with destination suggestion and reason.
    """
    # Simple logic for destination suggestions
    if "beach" in interest.lower():
        if "low" in budget.lower():
            return "Destination: Bali\nReason: Beautiful beaches with affordable options."
        elif "medium" in budget.lower():
            return "Destination: Maldives\nReason: Pristine beaches with mid-range resorts."
        else:
            return "Destination: Seychelles\nReason: Luxury beach experience with stunning scenery."
    elif "culture" in interest.lower():
        if "low" in budget.lower():
            return "Destination: Vietnam\nReason: Rich culture with budget-friendly options."
        elif "medium" in budget.lower():
            return "Destination: Italy\nReason: Cultural richness with mid-range accommodations."
        else:
            return "Destination: France\nReason: Ultimate cultural experience with luxury options."
    elif "adventure" in interest.lower():
        if "low" in budget.lower():
            return "Destination: Nepal\nReason: Adventure activities with low-cost options."
        elif "medium" in budget.lower():
            return "Destination: Costa Rica\nReason: Adventure activities with mid-range options."
        else:
            return "Destination: Switzerland\nReason: Adventure activities with luxury options."
    elif "food" in interest.lower():
        if "low" in budget.lower():
            return "Destination: Thailand\nReason: Amazing street food with budget options."
        elif "medium" in budget.lower():
            return "Destination: Mexico\nReason: Authentic cuisine with mid-range options."
        else:
            return "Destination: Japan\nReason: Gourmet cuisine with luxury dining options."
    else:  # Default case
        if "low" in budget.lower():
            return "Destination: Portugal\nReason: Great value for money with beautiful places."
        elif "medium" in budget.lower():
            return "Destination: Turkey\nReason: Great for families and mid-range budget."
        else:
            return "Destination: Greece\nReason: Luxury options with historical significance."


@tool
def famous_hotels(destination: str):
    """
    List famous hotels in a destination, categorized by budget range.

    Args:
        destination: The destination to find hotels for

    Returns:
        Structured string with hotel options by category.
    """
    destination_lower = destination.lower()

    if "bali" in destination_lower:
        return "Budget: Pondok Wisata Kori\nMid-range: The Haven Bali Seminyak\nLuxury: Four Seasons Resort Bali at Jimbaran Bay"
    elif "maldives" in destination_lower:
        return "Budget: Dhonakulhi Maldives\nMid-range: Angsana Ihuru\nLuxury: Soneva Fushi"
    elif "seychelles" in destination_lower:
        return "Budget: Le Passement\nMid-range: Constance Tharavadu\nLuxury: Four Seasons Resort Seychelles"
    elif "vietnam" in destination_lower:
        return "Budget: Hanoi Backpackers Hostel\nMid-range: Pullman Saigon Centre\nLuxury: Park Hyatt Saigon"
    elif "italy" in destination_lower:
        return "Budget: Yellow River Hostel Rome\nMid-range: Hotel Novecento\nLuxury: Hotel Danieli, Venice"
    elif "france" in destination_lower:
        return "Budget: Le Village Hostel Paris\nMid-range: Hotel National Des Arts\nLuxury: Le Meurice, Paris"
    elif "nepal" in destination_lower:
        return "Budget: Zostel Kathmandu\nMid-range: Hotel Vaishali\nLuxury: Dwarika's Hotel, Kathmandu"
    elif "costa rica" in destination_lower:
        return "Budget: Selina Hostel\nMid-range: Hotel Grano de Oro\nLuxury: Nayara Resort, Costa Rica"
    elif "switzerland" in destination_lower:
        return "Budget: Weggis Youth Hostel\nMid-range: Hotel Schweizerhof Luzern\nLuxury: Hotel Schweizerhof Bern"
    elif "thailand" in destination_lower:
        return "Budget: Lub d Bangkok Siam\nMid-range: Siam@Siam Design Hotel\nLuxury: Mandarin Oriental, Bangkok"
    elif "mexico" in destination_lower:
        return "Budget: Hostel Mundo Joven\nMid-range: Hotel Zocalo Central\nLuxury: Four Seasons Hotel Mexico City"
    elif "japan" in destination_lower:
        return "Budget: Khaosan Tokyo Origami\nMid-range: Hotel Sunroute Plaza Shinjuku\nLuxury: The Ritz-Carlton, Tokyo"
    elif "portugal" in destination_lower:
        return "Budget: Yes! Lisbon Hostel\nMid-range: HF Fenix Hotel\nLuxury: Belmond Reid's Palace"
    elif "turkey" in destination_lower:
        return "Budget: Sultan Ahmet Hostel\nMid-range: Hotel Amira Istanbul\nLuxury: Ciragan Palace Kempinski Istanbul"
    elif "greece" in destination_lower:
        return "Budget: Athens Backpackers\nMid-range: Electra Palace Athens\nLuxury: Canaves Oia Suites & Spa"
    else:
        # Default for unknown destinations
        return "Budget: Local Guesthouse\nMid-range: Regional Hotel\nLuxury: International Chain Hotel"


@tool
def famous_food(destination: str):
    """
    List famous local food in a destination.

    Args:
        destination: The destination to find food for

    Returns:
        Structured string with famous local food items.
    """
    destination_lower = destination.lower()

    if "bali" in destination_lower:
        return "Nasi Goreng, Babi Guling, Satay, Gado Gado"
    elif "maldives" in destination_lower:
        return "Garudhiya, Rihaakuru, Hedhikaa, Kibula"
    elif "seychelles" in destination_lower:
        return "Fish curry, Octopus salad, Coconut rum, Ladob"
    elif "vietnam" in destination_lower:
        return "Pho, Banh Mi, Bun Cha, Spring rolls"
    elif "italy" in destination_lower:
        return "Pizza, Pasta, Gelato, Risotto"
    elif "france" in destination_lower:
        return "Croissant, Baguette, Coq au Vin, Macarons"
    elif "nepal" in destination_lower:
        return "Dal Bhat, Momo, Thukpa, Sel Roti"
    elif "costa rica" in destination_lower:
        return "Gallo Pinto, Casado, Chifrijo, Tres Leches"
    elif "switzerland" in destination_lower:
        return "Rosti, Chocolate, Cheese fondue, Racclette"
    elif "thailand" in destination_lower:
        return "Pad Thai, Tom Yum Goong, Green curry, Mango sticky rice"
    elif "mexico" in destination_lower:
        return "Tacos, Guacamole, Mole, Churros"
    elif "japan" in destination_lower:
        return "Sushi, Ramen, Tempura, Wagyu beef"
    elif "portugal" in destination_lower:
        return "Pastel de nata, Bacalhau, Francesinha, Cozido"
    elif "turkey" in destination_lower:
        return "Kebab, Baklava, Meze, Turkish delight"
    elif "greece" in destination_lower:
        return "Gyros, Moussaka, Souvlaki, Tzatziki"
    else:
        # Default for unknown destinations
        return "Local specialties, Regional dishes, Traditional cuisine, Street food"


# Pydantic models for request/response
class DestinationRequest(BaseModel):
    travel_type: str
    budget: str
    interest: str


class HotelRequest(BaseModel):
    destination: str


class FoodRequest(BaseModel):
    destination: str


class HotelRequest(BaseModel):
    destination: str


class ToolResponse(BaseModel):
    result: str


# FastAPI app
app = FastAPI(
    title="Travel Agent API",
    description="Professional Travel Agent API with destination, hotel, and food recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Travel Agent API! Use /destination, /hotels, or /food endpoints."}


@app.post("/destination", response_model=ToolResponse)
def call_destination_finder(request: DestinationRequest):
    """
    Find travel destinations based on user preferences.
    """
    tool_func = tools["destination_finder"]
    result = tool_func(travel_type=request.travel_type, budget=request.budget, interest=request.interest)
    return ToolResponse(result=result)


@app.post("/hotels", response_model=ToolResponse)
def call_famous_hotels(request: HotelRequest):
    """
    List famous hotels in a destination.
    """
    tool_func = tools["famous_hotels"]
    result = tool_func(destination=request.destination)
    return ToolResponse(result=result)


@app.post("/food", response_model=ToolResponse)
def call_famous_food(request: FoodRequest):
    """
    List famous local food in a destination.
    """
    tool_func = tools["famous_food"]
    result = tool_func(destination=request.destination)
    return ToolResponse(result=result)


# Additional endpoint that tries to decide which tool to use based on input
class SmartRequest(BaseModel):
    user_input: str


@app.post("/smart", response_model=ToolResponse)
def smart_travel_assistant(request: SmartRequest):
    """
    Smart endpoint that decides which tool to use based on user input.
    """
    user_input = request.user_input.lower()

    # Determine tool based on keywords
    dest_keywords = ["travel", "where", "go", "destination", "trip", "vacation", "visit", "family", "budget", "interest"]
    hotel_keywords = ["hotel", "stay", "accommodation", "place to stay", "lodging", "resort"]
    food_keywords = ["food", "eat", "local food", "cuisine", "restaurant", "dishes"]

    if any(keyword in user_input for keyword in dest_keywords):
        # Extract basic info from input
        travel_type = "general"
        budget = "medium"
        interest = "general"

        if "family" in user_input or "family trip" in user_input:
            travel_type = "family"
        elif "romantic" in user_input or "honeymoon" in user_input:
            travel_type = "romantic"
        elif "solo" in user_input:
            travel_type = "solo"
        elif "business" in user_input:
            travel_type = "business"

        if "low" in user_input or "budget" in user_input or "cheap" in user_input or "affordable" in user_input:
            budget = "low"
        elif "high" in user_input or "luxury" in user_input or "expensive" in user_input:
            budget = "high"

        if "beach" in user_input:
            interest = "beach"
        elif "culture" in user_input or "history" in user_input:
            interest = "culture"
        elif "adventure" in user_input or "hiking" in user_input or "mountain" in user_input:
            interest = "adventure"
        elif "food" in user_input or "cuisine" in user_input:
            interest = "food"

        tool_func = tools["destination_finder"]
        result = tool_func(travel_type=travel_type, budget=budget, interest=interest)
        return ToolResponse(result=result)

    elif any(keyword in user_input for keyword in hotel_keywords):
        # Extract destination from input
        destinations = [
            "bali", "maldives", "seychelles", "vietnam", "italy", "france",
            "nepal", "costa rica", "switzerland", "thailand", "mexico",
            "japan", "portugal", "turkey", "greece"
        ]

        for dest in destinations:
            if dest in user_input:
                tool_func = tools["famous_hotels"]
                result = tool_func(destination=dest.title())
                return ToolResponse(result=result)

        # If no specific destination found, return error
        return ToolResponse(result="Please specify a destination for hotel recommendations.")

    elif any(keyword in user_input for keyword in food_keywords):
        # Extract destination from input
        destinations = [
            "bali", "maldives", "seychelles", "vietnam", "italy", "france",
            "nepal", "costa rica", "switzerland", "thailand", "mexico",
            "japan", "portugal", "turkey", "greece"
        ]

        for dest in destinations:
            if dest in user_input:
                tool_func = tools["famous_food"]
                result = tool_func(destination=dest.title())
                return ToolResponse(result=result)

        # If no specific destination found, return error
        return ToolResponse(result="Please specify a destination for food recommendations.")

    # Default to destination finder
    tool_func = tools["destination_finder"]
    result = tool_func(travel_type="general", budget="medium", interest="general")
    return ToolResponse(result=result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)