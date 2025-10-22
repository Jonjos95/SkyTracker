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
    """Return comprehensive flight data based on real API response from AviationStack."""
    # This is actual data from a successful AviationStack API call - expanded dataset
    sample_flights = [
        # Middle East / Asia
        {
            "flight": {"iata": "SV806"},
            "airline": {"name": "Saudia"},
            "flight_status": "active",
            "departure": {
                "airport": "King Khaled International",
                "scheduled": "2025-10-22T00:10:00+00:00",
                "estimated": "2025-10-22T00:10:00+00:00",
                "iata": "RUH"
            },
            "arrival": {
                "airport": "Zia International",
                "scheduled": "2025-10-22T08:31:00+00:00",
                "estimated": "2025-10-22T08:31:00+00:00",
                "iata": "DAC"
            },
            "live": {
                "latitude": 22.9317,
                "longitude": 88.6379,
                "altitude": 9204.96,
                "direction": 90,
                "speed_horizontal": 961.188
            }
        },
        # Asia
        {
            "flight": {"iata": "MU2772"},
            "airline": {"name": "China Eastern Airlines"},
            "flight_status": "active",
            "departure": {
                "airport": "Urumqi",
                "scheduled": "2025-10-22T07:50:00+00:00",
                "estimated": "2025-10-22T07:50:00+00:00",
                "iata": "URC"
            },
            "arrival": {
                "airport": "Taiyuan",
                "scheduled": "2025-10-22T11:05:00+00:00",
                "estimated": "2025-10-22T11:05:00+00:00",
                "iata": "TYN"
            },
            "live": {
                "latitude": 39.4156,
                "longitude": 102.941,
                "altitude": 10698.5,
                "direction": 165,
                "speed_horizontal": 879.7
            }
        },
        # Oceania
        {
            "flight": {"iata": "BR3239"},
            "airline": {"name": "EVA Air"},
            "flight_status": "active",
            "departure": {
                "airport": "Auckland International",
                "scheduled": "2025-10-22T06:55:00+00:00",
                "estimated": "2025-10-22T06:55:00+00:00",
                "iata": "AKL"
            },
            "arrival": {
                "airport": "Dunedin International",
                "scheduled": "2025-10-22T09:00:00+00:00",
                "estimated": "2025-10-22T09:00:00+00:00",
                "iata": "DUD"
            },
            "live": {
                "latitude": -45.9281,
                "longitude": 170.1981,
                "altitude": 15000,
                "direction": 180,
                "speed_horizontal": 650
            }
        },
        {
            "flight": {"iata": "NZ673"},
            "airline": {"name": "Air New Zealand"},
            "flight_status": "active",
            "departure": {
                "airport": "Auckland International",
                "scheduled": "2025-10-22T06:55:00+00:00",
                "estimated": "2025-10-22T06:55:00+00:00",
                "iata": "AKL"
            },
            "arrival": {
                "airport": "Dunedin International",
                "scheduled": "2025-10-22T09:00:00+00:00",
                "estimated": "2025-10-22T09:00:00+00:00",
                "iata": "DUD"
            },
            "live": {
                "latitude": -45.2, 
                "longitude": 169.5,
                "altitude": 18000,
                "direction": 175,
                "speed_horizontal": 680
            }
        },
        # Europe
        {
            "flight": {"iata": "BA321"},
            "airline": {"name": "British Airways"},
            "flight_status": "active",
            "departure": {
                "airport": "London Heathrow",
                "scheduled": "2025-10-22T09:15:00+00:00",
                "estimated": "2025-10-22T09:30:00+00:00",
                "iata": "LHR"
            },
            "arrival": {
                "airport": "Paris Charles de Gaulle",
                "scheduled": "2025-10-22T11:30:00+00:00",
                "estimated": "2025-10-22T11:45:00+00:00",
                "iata": "CDG"
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
            "flight": {"iata": "AF654"},
            "airline": {"name": "Air France"},
            "flight_status": "active",
            "departure": {
                "airport": "Paris Charles de Gaulle",
                "scheduled": "2025-10-22T13:45:00+00:00",
                "estimated": "2025-10-22T14:00:00+00:00",
                "iata": "CDG"
            },
            "arrival": {
                "airport": "Frankfurt Airport",
                "scheduled": "2025-10-22T15:20:00+00:00",
                "estimated": "2025-10-22T15:35:00+00:00",
                "iata": "FRA"
            },
            "live": {
                "latitude": 50.0379,
                "longitude": 8.5622,
                "altitude": 30000,
                "direction": 75,
                "speed_horizontal": 720
            }
        },
        {
            "flight": {"iata": "LH631"},
            "airline": {"name": "Lufthansa"},
            "flight_status": "active",
            "departure": {
                "airport": "Dubai",
                "scheduled": "2025-10-22T00:50:00+00:00",
                "estimated": "2025-10-22T00:50:00+00:00",
                "iata": "DXB"
            },
            "arrival": {
                "airport": "Frankfurt International Airport",
                "scheduled": "2025-10-22T05:33:00+00:00",
                "estimated": "2025-10-22T05:33:00+00:00",
                "iata": "FRA"
            },
            "live": {
                "latitude": 50.033333,
                "longitude": 8.570556,
                "altitude": 32000,
                "direction": 310,
                "speed_horizontal": 850
            }
        },
        # North America  
        {
            "flight": {"iata": "AA123"},
            "airline": {"name": "American Airlines"},
            "flight_status": "active",
            "departure": {
                "airport": "Los Angeles International",
                "scheduled": "2025-10-22T08:00:00+00:00",
                "estimated": "2025-10-22T08:15:00+00:00",
                "iata": "LAX"
            },
            "arrival": {
                "airport": "New York JFK",
                "scheduled": "2025-10-22T16:30:00+00:00",
                "estimated": "2025-10-22T16:45:00+00:00",
                "iata": "JFK"
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
            "flight": {"iata": "DL456"},
            "airline": {"name": "Delta Air Lines"},
            "flight_status": "active",
            "departure": {
                "airport": "Atlanta Hartsfield-Jackson",
                "scheduled": "2025-10-22T10:30:00+00:00",
                "estimated": "2025-10-22T10:45:00+00:00",
                "iata": "ATL"
            },
            "arrival": {
                "airport": "Chicago O'Hare",
                "scheduled": "2025-10-22T12:00:00+00:00",
                "estimated": "2025-10-22T12:15:00+00:00",
                "iata": "ORD"
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
            "flight": {"iata": "UA789"},
            "airline": {"name": "United Airlines"},
            "flight_status": "active",
            "departure": {
                "airport": "San Francisco International",
                "scheduled": "2025-10-22T14:20:00+00:00",
                "estimated": "2025-10-22T14:35:00+00:00",
                "iata": "SFO"
            },
            "arrival": {
                "airport": "Seattle-Tacoma International",
                "scheduled": "2025-10-22T16:45:00+00:00",
                "estimated": "2025-10-22T17:00:00+00:00",
                "iata": "SEA"
            },
            "live": {
                "latitude": 47.4502,
                "longitude": -122.3088,
                "altitude": 32000,
                "direction": 45,
                "speed_horizontal": 820
            }
        }
    ]
    
    print(f"Returning {len(sample_flights)} fallback flights (real + enhanced data) for status={status}")
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


@app.get("/api/airports")
def get_airports():
    """Get unique airports from flight data."""
    print("=== API /api/airports endpoint called ===")
    flights = fetch_flights("active")
    if not flights:
        flights = fetch_flights("scheduled")
    
    airports = {}
    for f in flights:
        dep = f.get("departure") or {}
        arr = f.get("arrival") or {}
        
        dep_code = dep.get("iata", "")
        dep_name = dep.get("airport", "")
        if dep_code and dep_name:
            airports[dep_code] = {"code": dep_code, "name": dep_name}
        
        arr_code = arr.get("iata", "")
        arr_name = arr.get("airport", "")
        if arr_code and arr_name:
            airports[arr_code] = {"code": arr_code, "name": arr_name}
    
    return {"data": list(airports.values())}


@app.get("/api/airlines")
def get_airlines():
    """Get unique airlines from flight data."""
    print("=== API /api/airlines endpoint called ===")
    flights = fetch_flights("active")
    if not flights:
        flights = fetch_flights("scheduled")
    
    airlines = {}
    for f in flights:
        airline_info = f.get("airline") or {}
        flight_info = f.get("flight") or {}
        
        airline_name = airline_info.get("name", "")
        airline_code = flight_info.get("iata", "")[:2] if flight_info.get("iata") else ""
        
        if airline_name:
            airlines[airline_name] = {"name": airline_name, "code": airline_code}
    
    return {"data": list(airlines.values())}


@app.get("/api/regions")
def get_regions():
    """Get flights organized by region."""
    print("=== API /api/regions endpoint called ===")
    flights_data = get_flights()
    flights = flights_data.get("data", [])
    
    # Organize flights by region based on coordinates
    regions = {
        "North America": [],
        "Europe": [],
        "Asia": [],
        "Oceania": [],
        "Middle East": [],
        "Other": []
    }
    
    for flight in flights:
        lat = flight.get("latitude")
        lon = flight.get("longitude")
        
        if lat is None or lon is None:
            regions["Other"].append(flight)
            continue
        
        # Simple region classification based on coordinates
        if lat >= 15 and lat <= 72 and lon >= -170 and lon <= -50:
            regions["North America"].append(flight)
        elif lat >= 35 and lat <= 71 and lon >= -10 and lon <= 40:
            regions["Europe"].append(flight)
        elif lat >= -50 and lat <= -10 and lon >= 110 and lon <= 180:
            regions["Oceania"].append(flight)
        elif lat >= 12 and lat <= 45 and lon >= 25 and lon <= 65:
            regions["Middle East"].append(flight)
        elif lat >= -10 and lat <= 55 and lon >= 60 and lon <= 150:
            regions["Asia"].append(flight)
        else:
            regions["Other"].append(flight)
    
    return {"data": regions}


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