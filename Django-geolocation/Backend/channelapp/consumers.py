# depots/consumers.py
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from geopy.distance import geodesic

@sync_to_async
def compute_top3(lat, lon):
    # ✅ import inside function to avoid AppRegistryNotReady
    from myapp.models import FuelDepot
    from myapp.serializers import FuelDepotSerializer

    user_point = (float(lat), float(lon))
    depots = FuelDepot.objects.all()
    depot_with_dist = []
    for d in depots:
        d_point = (d.latitude, d.longitude)
        dist_km = geodesic(user_point, d_point).km
        ser = FuelDepotSerializer(d).data
        ser["distance_km"] = round(dist_km, 3)
        depot_with_dist.append((ser, dist_km))

    depot_with_dist.sort(key=lambda x: x[1])
    return [item[0] for item in depot_with_dist[:3]]


class NearestDepotConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_json({"info": "connected"})

    async def receive_json(self, content, **kwargs):
        lat = content.get("lat")
        lon = content.get("lon")

        if lat is None or lon is None:
            await self.send_json({"error": "missing lat or lon"})
            return

        try:
            results = await compute_top3(lat, lon)
            await self.send_json({"results": results})
        except Exception as e:
            await self.send_json({"error": "server_error", "detail": str(e)})

    async def disconnect(self, code):
        pass
