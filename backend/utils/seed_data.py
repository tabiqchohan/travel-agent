from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.destination import Destination, TravelInterest, BudgetLevel, TravelType
from ..models.hotel import Hotel, HotelCategory
from ..models.food import FoodItem, FoodCategory


async def seed_destinations(db: AsyncSession):
    result = await db.execute(select(Destination).limit(1))
    if result.scalar_one_or_none():
        return

    destinations_data = [
        {
            "name": "Bali",
            "country": "Indonesia",
            "description": "A tropical paradise with stunning beaches, ancient temples, and vibrant culture. Known for its terraced rice paddies, coral reefs, and colorful festivals.",
            "interest": TravelInterest.BEACH,
            "budget_level": BudgetLevel.LOW,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "April to October",
            "currency": "IDR",
            "language": "Indonesian",
            "timezone": "UTC+8",
            "lat": -8.3405,
            "lng": 115.0920,
            "rating": 4.5,
        },
        {
            "name": "Maldives",
            "country": "Maldives",
            "description": "A tropical paradise of over 1,000 coral islands with pristine white-sand beaches, crystal-clear waters, and luxurious overwater bungalows.",
            "interest": TravelInterest.BEACH,
            "budget_level": BudgetLevel.MEDIUM,
            "travel_type": TravelType.ROMANTIC,
            "best_time_to_visit": "November to April",
            "currency": "MVR",
            "language": "Dhivehi",
            "timezone": "UTC+5",
            "lat": 3.2028,
            "lng": 73.2207,
            "rating": 4.7,
        },
        {
            "name": "Seychelles",
            "country": "Seychelles",
            "description": "An archipelago of 115 islands with stunning beaches, coral reefs, and unique wildlife. Perfect for luxury beach vacations.",
            "interest": TravelInterest.BEACH,
            "budget_level": BudgetLevel.HIGH,
            "travel_type": TravelType.ROMANTIC,
            "best_time_to_visit": "April to May, October to November",
            "currency": "SCR",
            "language": "Seychellois Creole",
            "timezone": "UTC+4",
            "lat": -4.6796,
            "lng": 55.4920,
            "rating": 4.6,
        },
        {
            "name": "Vietnam",
            "country": "Vietnam",
            "description": "A Southeast Asian gem with rich history, stunning landscapes from Ha Long Bay to terraced rice fields, and incredibly affordable travel options.",
            "interest": TravelInterest.CULTURE,
            "budget_level": BudgetLevel.LOW,
            "travel_type": TravelType.SOLO,
            "best_time_to_visit": "November to April",
            "currency": "VND",
            "language": "Vietnamese",
            "timezone": "UTC+7",
            "lat": 14.0583,
            "lng": 108.2772,
            "rating": 4.4,
        },
        {
            "name": "Italy",
            "country": "Italy",
            "description": "A country of unparalleled art, architecture, cuisine, and history. From Rome's ancient ruins to Venice's canals and Tuscany's rolling hills.",
            "interest": TravelInterest.CULTURE,
            "budget_level": BudgetLevel.MEDIUM,
            "travel_type": TravelType.ROMANTIC,
            "best_time_to_visit": "April to June, September to October",
            "currency": "EUR",
            "language": "Italian",
            "timezone": "UTC+1",
            "lat": 41.8719,
            "lng": 12.5674,
            "rating": 4.8,
        },
        {
            "name": "France",
            "country": "France",
            "description": "The world's most visited country, offering world-class art museums, culinary excellence, romantic cities, and beautiful countryside.",
            "interest": TravelInterest.CULTURE,
            "budget_level": BudgetLevel.HIGH,
            "travel_type": TravelType.ROMANTIC,
            "best_time_to_visit": "April to June, September to October",
            "currency": "EUR",
            "language": "French",
            "timezone": "UTC+1",
            "lat": 46.6034,
            "lng": 1.8883,
            "rating": 4.7,
        },
        {
            "name": "Nepal",
            "country": "Nepal",
            "description": "Home to eight of the world's ten tallest mountains, including Mount Everest. Offers trekking, adventure sports, and rich spiritual culture.",
            "interest": TravelInterest.ADVENTURE,
            "budget_level": BudgetLevel.LOW,
            "travel_type": TravelType.SOLO,
            "best_time_to_visit": "October to December, March to May",
            "currency": "NPR",
            "language": "Nepali",
            "timezone": "UTC+5:45",
            "lat": 28.3949,
            "lng": 84.1240,
            "rating": 4.3,
        },
        {
            "name": "Costa Rica",
            "country": "Costa Rica",
            "description": "A Central American paradise known for biodiversity, rainforests, volcanoes, and adventure activities like zip-lining, white-water rafting, and surfing.",
            "interest": TravelInterest.ADVENTURE,
            "budget_level": BudgetLevel.MEDIUM,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "December to April",
            "currency": "CRC",
            "language": "Spanish",
            "timezone": "UTC-6",
            "lat": 9.7489,
            "lng": -83.7534,
            "rating": 4.5,
        },
        {
            "name": "Switzerland",
            "country": "Switzerland",
            "description": "A stunning Alpine country offering world-class skiing, hiking trails, luxury resorts, chocolate, and breathtaking mountain scenery.",
            "interest": TravelInterest.ADVENTURE,
            "budget_level": BudgetLevel.HIGH,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "June to August, December to March",
            "currency": "CHF",
            "language": "German, French, Italian",
            "timezone": "UTC+1",
            "lat": 46.8182,
            "lng": 8.2275,
            "rating": 4.8,
        },
        {
            "name": "Thailand",
            "country": "Thailand",
            "description": "Famous for its incredible street food scene, beautiful beaches, ornate temples, and vibrant nightlife. A paradise for food lovers.",
            "interest": TravelInterest.FOOD,
            "budget_level": BudgetLevel.LOW,
            "travel_type": TravelType.SOLO,
            "best_time_to_visit": "November to February",
            "currency": "THB",
            "language": "Thai",
            "timezone": "UTC+7",
            "lat": 15.8700,
            "lng": 100.9925,
            "rating": 4.6,
        },
        {
            "name": "Mexico",
            "country": "Mexico",
            "description": "A vibrant country with rich culinary traditions, ancient Mayan ruins, beautiful beaches, and colorful festivals like Day of the Dead.",
            "interest": TravelInterest.FOOD,
            "budget_level": BudgetLevel.MEDIUM,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "December to April",
            "currency": "MXN",
            "language": "Spanish",
            "timezone": "UTC-6",
            "lat": 23.6345,
            "lng": -102.5528,
            "rating": 4.4,
        },
        {
            "name": "Japan",
            "country": "Japan",
            "description": "A fascinating blend of ancient traditions and cutting-edge technology. World-renowned for its gourmet cuisine, from sushi to ramen to kaiseki.",
            "interest": TravelInterest.FOOD,
            "budget_level": BudgetLevel.HIGH,
            "travel_type": TravelType.GENERAL,
            "best_time_to_visit": "March to May, October to November",
            "currency": "JPY",
            "language": "Japanese",
            "timezone": "UTC+9",
            "lat": 36.2048,
            "lng": 138.2529,
            "rating": 4.9,
        },
        {
            "name": "Portugal",
            "country": "Portugal",
            "description": "A beautiful country with stunning coastline, historic cities like Lisbon and Porto, delicious pastéis de nata, and great value for money.",
            "interest": TravelInterest.GENERAL,
            "budget_level": BudgetLevel.LOW,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "March to May, September to October",
            "currency": "EUR",
            "language": "Portuguese",
            "timezone": "UTC+0",
            "lat": 39.3999,
            "lng": -8.2245,
            "rating": 4.5,
        },
        {
            "name": "Turkey",
            "country": "Turkey",
            "description": "A transcontinental country bridging Europe and Asia with rich history, stunning architecture, delicious cuisine, and famous hot air balloon rides in Cappadocia.",
            "interest": TravelInterest.GENERAL,
            "budget_level": BudgetLevel.MEDIUM,
            "travel_type": TravelType.FAMILY,
            "best_time_to_visit": "April to June, September to November",
            "currency": "TRY",
            "language": "Turkish",
            "timezone": "UTC+3",
            "lat": 38.9637,
            "lng": 35.2433,
            "rating": 4.4,
        },
        {
            "name": "Greece",
            "country": "Greece",
            "description": "A country of ancient ruins, stunning islands with crystal-clear waters, and delicious Mediterranean cuisine. Perfect for history lovers and beach goers.",
            "interest": TravelInterest.GENERAL,
            "budget_level": BudgetLevel.HIGH,
            "travel_type": TravelType.ROMANTIC,
            "best_time_to_visit": "May to October",
            "currency": "EUR",
            "language": "Greek",
            "timezone": "UTC+2",
            "lat": 39.0742,
            "lng": 21.8243,
            "rating": 4.6,
        },
    ]

    for data in destinations_data:
        dest = Destination(**data)
        db.add(dest)

    await db.flush()
    destinations = await db.execute(select(Destination))
    dest_map = {d.name: d for d in destinations.scalars().all()}

    hotels_data = [
        {"destination": "Bali", "name": "Pondok Wisata Kori", "category": HotelCategory.BUDGET, "price_per_night": 25},
        {"destination": "Bali", "name": "The Haven Bali Seminyak", "category": HotelCategory.MID_RANGE, "price_per_night": 80},
        {"destination": "Bali", "name": "Four Seasons Resort Bali at Jimbaran Bay", "category": HotelCategory.LUXURY, "price_per_night": 350},
        {"destination": "Maldives", "name": "Dhonakulhi Maldives", "category": HotelCategory.BUDGET, "price_per_night": 100},
        {"destination": "Maldives", "name": "Angsana Ihuru", "category": HotelCategory.MID_RANGE, "price_per_night": 300},
        {"destination": "Maldives", "name": "Soneva Fushi", "category": HotelCategory.LUXURY, "price_per_night": 800},
        {"destination": "Thailand", "name": "Lub d Bangkok Siam", "category": HotelCategory.BUDGET, "price_per_night": 20},
        {"destination": "Thailand", "name": "Siam@Siam Design Hotel", "category": HotelCategory.MID_RANGE, "price_per_night": 70},
        {"destination": "Thailand", "name": "Mandarin Oriental Bangkok", "category": HotelCategory.LUXURY, "price_per_night": 400},
        {"destination": "Japan", "name": "Khaosan Tokyo Origami", "category": HotelCategory.BUDGET, "price_per_night": 30},
        {"destination": "Japan", "name": "Hotel Sunroute Plaza Shinjuku", "category": HotelCategory.MID_RANGE, "price_per_night": 120},
        {"destination": "Japan", "name": "The Ritz-Carlton Tokyo", "category": HotelCategory.LUXURY, "price_per_night": 600},
    ]

    for hdata in hotels_data:
        dest = dest_map.get(hdata["destination"])
        if dest:
            hotel = Hotel(destination_id=dest.id, name=hdata["name"], category=hdata["category"], price_per_night=hdata["price_per_night"])
            db.add(hotel)

    food_data = [
        {"destination": "Thailand", "name": "Pad Thai", "category": FoodCategory.MAIN_DISH, "price_range": "$2-5", "spice_level": "medium"},
        {"destination": "Thailand", "name": "Tom Yum Goong", "category": FoodCategory.MAIN_DISH, "price_range": "$3-6", "spice_level": "hot"},
        {"destination": "Thailand", "name": "Green Curry", "category": FoodCategory.MAIN_DISH, "price_range": "$3-5", "spice_level": "hot"},
        {"destination": "Thailand", "name": "Mango Sticky Rice", "category": FoodCategory.DESSERT, "price_range": "$2-4", "spice_level": "mild"},
        {"destination": "Japan", "name": "Sushi", "category": FoodCategory.MAIN_DISH, "price_range": "$10-50", "spice_level": "mild"},
        {"destination": "Japan", "name": "Ramen", "category": FoodCategory.MAIN_DISH, "price_range": "$8-15", "spice_level": "medium"},
        {"destination": "Japan", "name": "Tempura", "category": FoodCategory.MAIN_DISH, "price_range": "$10-20", "spice_level": "mild"},
        {"destination": "Japan", "name": "Wagyu Beef", "category": FoodCategory.MAIN_DISH, "price_range": "$50-200", "spice_level": "mild"},
        {"destination": "Italy", "name": "Pizza", "category": FoodCategory.MAIN_DISH, "price_range": "$8-20", "spice_level": "mild"},
        {"destination": "Italy", "name": "Pasta", "category": FoodCategory.MAIN_DISH, "price_range": "$10-25", "spice_level": "mild"},
        {"destination": "Italy", "name": "Gelato", "category": FoodCategory.DESSERT, "price_range": "$3-6", "spice_level": "mild"},
        {"destination": "Italy", "name": "Risotto", "category": FoodCategory.MAIN_DISH, "price_range": "$12-30", "spice_level": "mild"},
    ]

    for fdata in food_data:
        dest = dest_map.get(fdata["destination"])
        if dest:
            food = FoodItem(
                destination_id=dest.id,
                name=fdata["name"],
                category=fdata["category"],
                price_range=fdata["price_range"],
                spice_level=fdata.get("spice_level"),
            )
            db.add(food)

    await db.commit()
