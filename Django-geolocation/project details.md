# 🚚 Live Nearest Fuel Depot Tracker (Frontend + Backend)

This project provides a **real-time fuel depot finder** that detects the user's live location and continuously fetches the nearest fuel depot from a Django backend. The frontend displays this on an interactive map and draws a driving route using OSRM.

---

## 🔩 How It Works — Architecture Overview

[ Browser Frontend ]
|
| (GET /api/nearest-depot/?lat=&lon=)
v
[ Django Backend ]
|
| Returns nearest depot info (lat, lon, distance)
v
[ PostGIS / Geo DB with depot locations ]

yaml
Copy code

---

## 🖥 Frontend — What It Does

1. Uses `navigator.geolocation.watchPosition()` to track the user live  
2. Throttles API requests (e.g., one request every 5 seconds)
3. Sends live coordinates to  
GET /api/nearest-depot/?lat=<lat>&lon=<lon>

pgsql
Copy code
4. Receives nearest depot data from backend  
```json
{
  "id": 12,
  "name": "HP Fuel Depot — Sector 5",
  "latitude": 22.5991,
  "longitude": 88.4319,
  "distance_km": 3.42
}
Updates map in real time:

Blue marker = user

Red marker = nearest depot

Uses Leaflet Routing Machine to draw route using OSRM

Includes auto fallback manual simulation if GPS fails

Generates fake movement for development/testing

🧾 Backend — What It Does
Receives live user coordinates from frontend

Calculates distance to all depots (usually using GeoDjango / geopy / PostGIS)

Finds the nearest depot using Haversine or spatial query

Returns JSON response:

Depot name

Depot coordinates

Distance in kilometers

Example Django view (concept):

python
Copy code
def nearest_depot(request):
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    # compute nearest depot using DB or geopy
    return JsonResponse({
       "id": depot.id,
       "name": depot.name,
       "latitude": depot.lat,
       "longitude": depot.lon,
       "distance_km": distance
    })
✅ Key Features
Real-time location tracking

Distance calculated server-side

Driving route displayed using OSRM

Works with or without GPS (manual test mode fallback)

Fully decoupled: backend API + HTML/JS frontend

🔮 Future Enhancements (Possible)
Show list of top 3 nearest depots

Add ETA / travel time

Show fuel types & availability (diesel/petrol)

Driver authentication & session tracking

WebSocket live push updates instead of polling

📌 Summary
This project is a complete end-to-end solution for real-time nearest fuel depot detection.
It is useful for logistics, delivery fleets, emergency refueling, or public utility dashboards.

yaml
Copy code

---

If you want I can now:
- Generate a `README.md` file for GitHub with badges and sections
- Add API documentation section for `/api/nearest-depot`
- Add diagrams or screenshots

Tell me what to add next.