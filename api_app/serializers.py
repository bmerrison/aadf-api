from rest_framework import serializers
from api_app.models import Junction

class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ('id', 'description')
