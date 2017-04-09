from rest_framework import viewsets

from api_app.models import Junction, \
    EstimationMethod, \
    Region

from api_app.serializers import JunctionSerializer, \
    EstimationMethodSerializer, \
    RegionSerializer

class JunctionViewSet(viewsets.ModelViewSet):
    queryset = Junction.objects.all()
    serializer_class = JunctionSerializer

class EstimationMethodViewSet(viewsets.ModelViewSet):
    queryset = EstimationMethod.objects.all()
    serializer_class = EstimationMethodSerializer
    
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
