from rest_framework import serializers
from api_app.models import Junction, \
    EstimationMethod, \
    Region

class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ('id', 'description')

class EstimationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationMethod
        fields = ('id', 'description')
        
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')
