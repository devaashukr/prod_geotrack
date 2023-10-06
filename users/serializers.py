from rest_framework import serializers

class LocationDataSerializer(serializers.Serializer):
    systime = serializers.IntegerField()
    exceptionBM = serializers.IntegerField()
    virtualName = serializers.CharField()
    speed = serializers.DecimalField(max_digits=10, decimal_places=2)
    direction = serializers.IntegerField()
    haltedSince = serializers.CharField()
    elevation = serializers.DecimalField(max_digits=10, decimal_places=2)
    timestamp = serializers.IntegerField()
    distance = serializers.DecimalField(max_digits=10, decimal_places=2)
    locStr = serializers.CharField()
    noDataSince = serializers.CharField()
    lattitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    movingSince = serializers.CharField()
    longitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    regNo = serializers.CharField()
    bmStr = serializers.CharField()

class VehicleSerializer(serializers.Serializer):
    vehicle_data = serializers.ListField(
        child=LocationDataSerializer()
    )

class VehicleLocationSerializer(serializers.Serializer):
    # Assuming you have multiple vehicles, wrap each vehicle in a list
    vehicles = serializers.ListField(
        child=VehicleSerializer()
    )