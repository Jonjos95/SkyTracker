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


def fetch_flights(status: str):
    """Fetch flights from AviationStack API."""
    try:
        params = {
            "access_key": API_KEY,
            "flight_status": status,
            "limit": 50
        }
        response = requests.get(BASE_URL, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        flights = data.get("data", [])
        print(f"Fetched {len(flights)} flights with status={status}")
        return flights
    except Exception as e:
        print("Error fetching flights:", e)
        return []


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


# --- Serve Frontend Static Files ---
app.mount("/", StaticFiles(directory=".", html=True), name="static")


# --- Hugging Face Spaces compatibility ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))  # Hugging Face Spaces uses port 7860
    print(f"===== Application Startup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} =====")
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)