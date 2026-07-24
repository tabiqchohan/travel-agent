# Travel Agent - Your Personal Travel Assistant

A comprehensive travel recommendation system with both API backend and user-friendly frontend.

## Features

- **Destination Finder**: Find travel destinations based on travel type, budget, and interests
- **Hotel Recommendations**: Get hotel suggestions by destination and budget range
- **Local Food Guide**: Discover famous local foods in various destinations
- **Smart Assistant**: Natural language travel recommendations
- **Web Interface**: User-friendly frontend to interact with all features

## Supported Destinations

- Beach Destinations: Bali, Maldives, Seychelles
- Cultural Destinations: Vietnam, Italy, France
- Adventure Destinations: Nepal, Costa Rica, Switzerland
- Food Destinations: Thailand, Mexico, Japan
- General Destinations: Portugal, Turkey, Greece

## Getting Started

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**:
   - Option 1 - With Frontend: Run the combined server
     ```bash
     python server.py
     ```

   - Option 2 - API Only: Run the original server
     ```bash
     python main.py
     # or
     uvicorn main:app --reload
     ```

3. **Access the Application**:
   - **Frontend Interface**: [http://localhost:8080](http://localhost:8080)
   - **API Documentation**: [http://localhost:8080/api/docs](http://localhost:8080/api/docs)
   - **API Redoc**: [http://localhost:8080/api/redoc](http://localhost:8080/api/redoc)

## Using the Travel Agent

### 1. Web Interface (Recommended for End Users)

Access [http://localhost:8000](http://localhost:8000) for a user-friendly interface with:

- **Find Destinations**: Select travel type, budget, and interests
- **Find Hotels**: Enter a destination to get hotel recommendations
- **Find Food**: Enter a destination to discover local cuisine
- **Smart Assistant**: Describe your travel needs in natural language

### 2. Direct API Usage

You can also use the API endpoints directly:

#### Destination Finder
```bash
curl -X POST "http://localhost:8000/api/destination" \
  -H "Content-Type: application/json" \
  -d '{"travel_type": "family", "budget": "medium", "interest": "beach"}'
```

#### Hotel Finder
```bash
curl -X POST "http://localhost:8000/api/hotels" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Bali"}'
```

#### Food Finder
```bash
curl -X POST "http://localhost:8000/api/food" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Thailand"}'
```

#### Smart Assistant
```bash
curl -X POST "http://localhost:8000/api/smart" \
  -H "Content-Type: application/json" \
  -d '{"user_input": "I want to go somewhere with my family on a budget, interested in beach destinations"}'
```

## Example Queries

- "I want to go on a family beach vacation with a moderate budget"
- "Show me luxury hotels in Italy"
- "What are famous foods in Japan?"
- "I'm planning a romantic trip with high budget and cultural interest"
- "Where can I go for adventure travel on a low budget?"

## Project Structure

- `main.py`: Core FastAPI backend with travel recommendation tools
- `server.py`: Combined server for API and frontend
- `index.html`: User-friendly frontend interface
- `requirements.txt`: Python dependencies
- `README.md`: This file