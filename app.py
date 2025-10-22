from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os
from datetime import datetime

app = FastAPI()

# --- Middleware to allow frontend requests ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Configuration ---
API_KEY = "7776ec316291c9bc34c8f7b80f217f08"
BASE_URL = "https://api.aviationstack.com/v1/flights"


def get_fallback_flights(status: str):
    """Return sample flight data when API is unavailable."""
    sample_flights = [
        {
            "flight": {"iata": "AA123", "icao": "AAL123"},
            "airline": {"name": "American Airlines"},
            "flight_status": "active",
            "departure": {
                "airport": "Los Angeles International",
                "scheduled": "2025-10-22T08:00:00+00:00",
                "estimated": "2025-10-22T08:15:00+00:00"
            },
            "arrival": {
                "airport": "New York JFK",
                "scheduled": "2025-10-22T16:30:00+00:00",
                "estimated": "2025-10-22T16:45:00+00:00"
            },
            "live": {
                "latitude": 40.6892,
                "longitude": -74.0445,
                "altitude": 35000,
                "direction": 90,
                "speed_horizontal": 850
            }
        },
        {
            "flight": {"iata": "DL456", "icao": "DAL456"},
            "airline": {"name": "Delta Air Lines"},
            "flight_status": "active",
            "departure": {
                "airport": "Atlanta Hartsfield-Jackson",
                "scheduled": "2025-10-22T10:30:00+00:00",
                "estimated": "2025-10-22T10:45:00+00:00"
            },
            "arrival": {
                "airport": "Chicago O'Hare",
                "scheduled": "2025-10-22T12:00:00+00:00",
                "estimated": "2025-10-22T12:15:00+00:00"
            },
            "live": {
                "latitude": 41.9786,
                "longitude": -87.9048,
                "altitude": 28000,
                "direction": 315,
                "speed_horizontal": 780
            }
        },
        {
            "flight": {"iata": "UA789", "icao": "UAL789"},
            "airline": {"name": "United Airlines"},
            "flight_status": "active",
            "departure": {
                "airport": "San Francisco International",
                "scheduled": "2025-10-22T14:20:00+00:00",
                "estimated": "2025-10-22T14:35:00+00:00"
            },
            "arrival": {
                "airport": "Seattle-Tacoma International",
                "scheduled": "2025-10-22T16:45:00+00:00",
                "estimated": "2025-10-22T17:00:00+00:00"
            },
            "live": {
                "latitude": 47.4502,
                "longitude": -122.3088,
                "altitude": 32000,
                "direction": 45,
                "speed_horizontal": 820
            }
        },
        {
            "flight": {"iata": "BA321", "icao": "BAW321"},
            "airline": {"name": "British Airways"},
            "flight_status": "active",
            "departure": {
                "airport": "London Heathrow",
                "scheduled": "2025-10-22T09:15:00+00:00",
                "estimated": "2025-10-22T09:30:00+00:00"
            },
            "arrival": {
                "airport": "Paris Charles de Gaulle",
                "scheduled": "2025-10-22T11:30:00+00:00",
                "estimated": "2025-10-22T11:45:00+00:00"
            },
            "live": {
                "latitude": 49.0097,
                "longitude": 2.5479,
                "altitude": 25000,
                "direction": 180,
                "speed_horizontal": 650
            }
        },
        {
            "flight": {"iata": "AF654", "icao": "AFR654"},
            "airline": {"name": "Air France"},
            "flight_status": "active",
            "departure": {
                "airport": "Paris Charles de Gaulle",
                "scheduled": "2025-10-22T13:45:00+00:00",
                "estimated": "2025-10-22T14:00:00+00:00"
            },
            "arrival": {
                "airport": "Frankfurt Airport",
                "scheduled": "2025-10-22T15:20:00+00:00",
                "estimated": "2025-10-22T15:35:00+00:00"
            },
            "live": {
                "latitude": 50.0379,
                "longitude": 8.5622,
                "altitude": 30000,
                "direction": 75,
                "speed_horizontal": 720
            }
        }
    ]
    
    print(f"Returning {len(sample_flights)} fallback flights for status={status}")
    return sample_flights


def fetch_flights(status: str):
    """Fetch flights from AviationStack API."""
    try:
        params = {
            "access_key": API_KEY,
            "flight_status": status,
            "limit": 50
        }
        response = requests.get(BASE_URL, params=params, timeout=20)
        
        if response.status_code == 429:
            print(f"Rate limit exceeded (429). Using fallback data for status={status}")
            return get_fallback_flights(status)
        
        response.raise_for_status()
        data = response.json()
        flights = data.get("data", [])
        print(f"Fetched {len(flights)} flights with status={status}")
        return flights
    except Exception as e:
        print(f"Error fetching flights for {status}:", e)
        print(f"Using fallback data for status={status}")
        return get_fallback_flights(status)


@app.get("/health")
def health_check():
    """Health check endpoint for Hugging Face Spaces."""
    return {"status": "healthy", "message": "SkyTracker API is running"}

@app.get("/flights")
def get_flights():
    """Fetch and normalize flight data for frontend."""
    print("=== API /flights endpoint called ===")
    flights = fetch_flights("active")

    # fallback to scheduled if no active
    if not flights:
        flights = fetch_flights("scheduled")

    clean_data = []
    for f in flights:
        # --- Extract Airline ---
        airline_info = f.get("airline") or {}
        airline = airline_info.get("name") or "Unknown Airline"

        # --- Extract Flight ---
        flight_info = f.get("flight") or {}
        codeshared = flight_info.get("codeshared") or {}
        flight_iata = (
            flight_info.get("iata")
            or codeshared.get("flight_iata")
            or flight_info.get("icao")
            or "N/A"
        )

        # --- Extract Status ---
        status = (f.get("flight_status") or "Unknown").capitalize()

        # --- Extract Departure / Arrival ---
        dep = f.get("departure") or {}
        arr = f.get("arrival") or {}

        departure_airport = dep.get("airport") or "Unknown"
        arrival_airport = arr.get("airport") or "Unknown"

        dep_time = dep.get("estimated") or dep.get("scheduled") or "N/A"
        arr_time = arr.get("estimated") or arr.get("scheduled") or "N/A"

        # --- Extract Live Data ---
        live = f.get("live") or {}
        latitude = live.get("latitude")
        longitude = live.get("longitude")
        altitude = live.get("altitude")
        direction = live.get("direction")
        speed_horizontal = live.get("speed_horizontal")

        # --- Normalize Filtering ---
        # Keep all flights, even if lat/lon missing — don't discard
        clean_data.append({
            "flight_iata": flight_iata,
            "airline": airline,
            "status": status,
            "departure": departure_airport,
            "arrival": arrival_airport,
            "dep_time": dep_time,
            "arr_time": arr_time,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "direction": direction,
            "speed": speed_horizontal
        })

    # --- Debug Preview ---
    print(json.dumps(clean_data[:3], indent=2))
    return {"data": clean_data}


# --- Root route for Hugging Face Spaces ---
@app.get("/")
async def read_root():
    """Serve the main index.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("index.html")

@app.get("/index.html")
async def read_index():
    """Serve the main index.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("index.html")

@app.get("/livemap.html")
async def read_livemap():
    """Serve the livemap.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("livemap.html")

@app.get("/airports.html")
async def read_airports():
    """Serve the airports.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("airports.html")

@app.get("/airlines.html")
async def read_airlines():
    """Serve the airlines.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("airlines.html")

@app.get("/saved.html")
async def read_saved():
    """Serve the saved.html file."""
    from fastapi.responses import FileResponse
    return FileResponse("saved.html")

# --- Serve other static files ---
app.mount("/static", StaticFiles(directory="."), name="static")


# --- Hugging Face Spaces compatibility ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face Spaces uses port 7860
    print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)