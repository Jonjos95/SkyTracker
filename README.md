---
title: SkyTracker Pro - Live Flight Tracking
emoji: ✈️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: Real-time flight tracking with interactive maps
app_port: 7860
---

# SkyTracker Pro - Live Flight Tracking

A real-time flight tracking application that displays live flight data from around the world with interactive maps and detailed flight information.

## Features

- ✈️ **Live Flight Data**: Real-time tracking of active flights worldwide
- 🗺️ **Interactive Maps**: Visual representation of flights on an interactive map
- 📊 **Flight Details**: Comprehensive flight information including airlines, routes, and status
- 🔍 **Search & Filter**: Search through flights by airline, route, or flight number
- 📱 **Responsive Design**: Beautiful, modern UI that works on all devices
- ⚡ **Real-time Updates**: Automatic data refresh every 30 seconds

## API Endpoints

- `GET /flights` - Returns live flight data in JSON format
- `GET /` - Serves the main application interface
- `GET /livemap.html` - Interactive flight map
- `GET /docs` - FastAPI auto-generated documentation

## Data Sources

Flight data is powered by the [AviationStack API](https://aviationstack.com/), providing real-time information about:
- Flight status and tracking
- Airport information
- Airline details
- Live coordinates and flight paths

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Maps**: Leaflet.js
- **Visual Effects**: Vanta.js
- **Icons**: Feather Icons

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser to `http://localhost:8000`

## Deployment

This application is configured for deployment on Hugging Face Spaces using Docker. The app automatically adapts to the PORT environment variable for cloud deployment.

## License

MIT License - feel free to use this project for your own flight tracking applications!