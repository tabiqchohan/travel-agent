import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@pytest.mark.asyncio
async def test_list_destinations(client):
    response = await client.get("/api/v1/destinations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_search_destinations(client):
    response = await client.get("/api/v1/destinations/search?interest=beach&budget=low")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_smart_assistant(client):
    response = await client.post(
        "/api/v1/smart",
        json={"user_input": "I want a family beach vacation on a budget"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "result" in data


@pytest.mark.asyncio
async def test_budget_estimate(client):
    response = await client.post(
        "/api/v1/budget/estimate",
        json={
            "destination": "Bali",
            "origin": "New York",
            "duration_days": 7,
            "travelers": 2,
            "hotel_category": "mid_range",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_estimated_cost"] > 0
    assert "breakdown" in data


@pytest.mark.asyncio
async def test_hotels(client):
    response = await client.get("/api/v1/hotels?destination=Bali")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_food(client):
    response = await client.get("/api/v1/food?destination=Thailand")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
