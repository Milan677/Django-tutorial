from geopy.distance import geodesic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FuelDepot
from .serializers import FuelDepotSerializer

@api_view(['GET'])
def nearest_depot(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return Response({"error": "lat and lon required"}, status=status.HTTP_400_BAD_REQUEST)

    user_point = (float(lat), float(lon))

    depots = FuelDepot.objects.all()
    if not depots.exists():
        return Response({"error": "No depots in database"}, status=404)

    nearest = None
    min_dist = float("inf")

    for d in depots:
        depot_point = (d.latitude, d.longitude)
        dist_km = geodesic(user_point, depot_point).km
        if dist_km < min_dist:
            min_dist = dist_km
            nearest = d

    nearest.distance_km = min_dist
    serializer = FuelDepotSerializer(nearest)
    return Response(serializer.data)



from geopy.distance import geodesic
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FuelDepot
from .serializers import FuelDepotSerializer

@api_view(['GET'])
def nearest_three_depot(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return Response({"error": "lat and lon required"}, status=400)

    user_point = (float(lat), float(lon))

    depots = FuelDepot.objects.all()
    if not depots.exists():
        return Response({"error": "No depots in database"}, status=404)

    # --- compute distance for each depot ---
    depot_with_dist = []
    for d in depots:
        d_point = (d.latitude, d.longitude)
        dist_km = geodesic(user_point, d_point).km
        depot_with_dist.append((d, dist_km))

    # --- sort by distance ---
    depot_with_dist.sort(key=lambda x: x[1])

    # --- take top 3 ---
    top3 = depot_with_dist[:3]

    # --- serialize and attach distance in response ---
    data = []
    for depot, dist in top3:
        ser = FuelDepotSerializer(depot).data
        ser['distance_km'] = round(dist, 3)
        data.append(ser)

    return Response({"results": data})
