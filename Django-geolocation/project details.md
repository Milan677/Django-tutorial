# ⛽ Live Nearest Fuel Depot Tracker  
Real-time user tracking + nearest depot API + route visualization

---

## 🚀 Overview

This project continuously tracks the user's live location in the browser and calls a Django backend API to fetch the **nearest fuel depot**.  
The frontend displays:
- The user's real-time location on a Leaflet map  
- The nearest depot marker  
- A live driving route using OSRM (Leaflet Routing Machine)  

If GPS access is blocked or unavailable, the app automatically switches to **Manual Simulation Mode** that mimics user movement for testing.

---

## 🧠 System Architecture

[ Browser Frontend (Leaflet + JS) ]
│ watchPosition() + throttled GET
▼
GET /api/nearest-depot/?lat=..&lon=..
▼
[ Django Backend ]
│ computes nearest depot (geopy/PostGIS)
▼
JSON: name, coords, distance_km

yaml
Copy code

---

## 🖥 Frontend — Key Responsibilities

✅ Uses `navigator.geolocation.watchPosition()` for live tracking  
✅ Throttles API calls (prevents spam / high server load)  
✅ Sends current `lat, lon` to backend  
✅ Draws user marker + depot marker  
✅ Draws route between user and depot using `Leaflet Routing Machine`  
✅ Auto-fallback to **manual simulation** when GPS fails  

---

## 🧾 Backend — Key Responsibilities

✅ Receives `lat, lon` via query params from frontend  
✅ Calculates distances to fuel depots (via geopy or PostGIS)  
✅ Finds the nearest depot  
✅ Returns JSON response like:

```json
{
  "id": 12,
  "name": "HP Fuel Depot — Sector 5",
  "latitude": 22.5991,
  "longitude": 88.4319,
  "distance_km": 3.42
}
```
🔁 API Contract
Request

bash
Copy code
GET /api/nearest-depot/?lat=<float>&lon=<float>
Response 200

json
Copy code
{
  "id": 1,
  "name": "Indian Oil Depot — Park Circus",
  "latitude": 22.5531,
  "longitude": 88.3632,
  "distance_km": 2.85
}
## 🧩 Features Summary
Feature	Description
Live tracking	Uses browser GPS + watchPosition()
API throttling	Prevents rapid backend calls
Manual Test Mode	Auto fallback when GPS blocked
Routing	Draws actual drive route via OSRM
Stateless	Decoupled frontend & Django backend

## 📌 Possible Next Enhancements
Show multiple nearest depots

Show ETA (minutes) instead of just distance

Store user tracking history

WebSockets for push-based updates

Authentication for delivery fleets

## ✅ Use Cases
Fuel delivery fleets and logistics

Emergency fuel service tracking

Fleet management dashboards

Navigation-assisted refueling applications

## 📜 License
This project is provided as an architectural reference.
You are free to modify and use it for your own applications.

