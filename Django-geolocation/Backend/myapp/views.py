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
