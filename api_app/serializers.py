from rest_framework import serializers
from api_app.models import Junction, \
    EstimationMethod, \
    Region, \
    LocalAuthority

class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ('id', 'description')

class EstimationMethodSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = EstimationMethod
        fields = ('id', 'description', )
        
class RegionSerializer(serializers.ModelSerializer):
    local_authorities = serializers.PrimaryKeyRelatedField(
        many=True,
        default=[],
        queryset=LocalAuthority.objects.all())
        
    class Meta:
        model = Region
        fields = ('id', 'name', 'local_authorities')

class LocalAuthoritySerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    
    class Meta:
        model = LocalAuthority
        fields = ('id', 'name', 'region', 'region_name')        
