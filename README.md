# Travel Agent Pro v2.0

Advanced travel recommendation system with FastAPI backend, modern frontend, JWT auth, AI-powered Smart Assistant (Groq), trip planner, budget calculator, interactive maps, and more.

## Features

- **Destination Finder** — Search by travel type, budget, interest
- **Hotel Recommendations** — Budget/Mid-range/Luxury categories
- **Local Food Guide** — Discover local cuisine worldwide
- **AI Smart Assistant** — Natural language processing (Groq LLM)
- **Trip Planner** — Multi-day itinerary builder with activities
- **Budget Calculator** — Estimate total trip cost (flight, hotel, food, activities)
- **Weather Forecast** — Real-time weather data (OpenWeatherMap)
- **User Auth** — JWT-based registration/login
- **Reviews & Ratings** — User reviews with star ratings
- **Favorites/Wishlist** — Save destinations
- **Interactive Maps** — OpenStreetMap + Leaflet

## Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file (copy from .env.example)
#    Minimum: SECRET_KEY=your-random-key

# 3. Run with frontend
python server.py
# → http://localhost:8080

# 4. Or API only
uvicorn backend.main:app --reload
# → http://localhost:8000/api/v1/docs
```

## Deployment

### Backend → Render

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Fill:

   | Field | Value |
   |-------|-------|
   | **Runtime** | Python |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | Free |

5. Add Environment Variables:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL_POSTGRES` | `postgresql+asyncpg://user:pass@host/db` (from [Neon](https://neon.tech)) |
   | `SECRET_KEY` | random string |
   | `GROQ_API_KEY` | (optional) from [console.groq.com](https://console.groq.com) |
   | `OPENWEATHER_API_KEY` | (optional) from [openweathermap.org](https://openweathermap.org) |
   | `DEBUG` | `false` |

6. Deploy! Get your URL like `https://travel-agent-api.onrender.com`

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo
3. **Framework Preset**: Other
4. **Root Directory**: `./` (default)
5. Add Environment Variable:

   | Key | Value |
   |-----|-------|
   | `RENDER_URL` | `https://your-app.onrender.com` (from step above) |

6. Deploy!

> **Note:** The frontend will use the `RENDER_URL` env var to call the backend API. Locally it auto-detects `localhost`.

## Project Structure

```
├── backend/
│   ├── main.py         — FastAPI app (entry point)
│   ├── config.py       — Settings via .env
│   ├── database.py     — SQLAlchemy async engine
│   ├── models/         — 8 database models
│   ├── schemas/        — Pydantic request/response schemas
│   ├── routers/        — 10 API route modules
│   ├── services/       — Business logic
│   └── utils/          — Security, seed data
├── index.html          — Frontend (Tailwind CSS + Leaflet)
├── server.py           — Combined local dev server
├── vercel.json         — Vercel frontend config
├── render.yaml         — Render IaC config
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/health` | Health check |
| `POST /api/v1/auth/register` | Register user |
| `POST /api/v1/auth/login` | Login |
| `GET /api/v1/destinations` | List all destinations |
| `GET /api/v1/destinations/search` | Search destinations |
| `GET /api/v1/hotels?destination=X` | Find hotels |
| `GET /api/v1/food?destination=X` | Find food |
| `POST /api/v1/smart` | AI smart assistant |
| `POST /api/v1/trips` | Create trip (auth) |
| `POST /api/v1/budget/estimate` | Budget calculator |
| `GET /api/v1/weather?destination=X` | Weather forecast |
| `POST /api/v1/reviews` | Add review (auth) |
| `POST /api/v1/favorites` | Add favorite (auth) |
