from rest_framework import serializers
from api_app.models import Junction, EstimationMethod

class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ('id', 'description')

class EstimationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimationMethod
        fields = ('id', 'description')
        
