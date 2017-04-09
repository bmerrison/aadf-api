from rest_framework import viewsets

from api_app.models import Junction, \
    EstimationMethod, \
    Region, \
    LocalAuthority

from api_app.serializers import JunctionSerializer, \
    EstimationMethodSerializer, \
    RegionSerializer, \
    LocalAuthoritySerializer

class JunctionViewSet(viewsets.ModelViewSet):
    queryset = Junction.objects.all()
    serializer_class = JunctionSerializer

class EstimationMethodViewSet(viewsets.ModelViewSet):
    queryset = EstimationMethod.objects.all()
    serializer_class = EstimationMethodSerializer
    
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class LocalAuthorityViewSet(viewsets.ModelViewSet):
    queryset = LocalAuthority.objects.all()
    serializer_class = LocalAuthoritySerializer
    
    
