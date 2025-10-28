from rest_framework import serializers
from .models import FuelDepot

class FuelDepotSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = FuelDepot
        fields = ['id', 'name', 'latitude', 'longitude', 'distance_km']
