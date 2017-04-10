from rest_framework import viewsets

from api_app.models import Junction, \
    EstimationMethod, \
    Region, \
    LocalAuthority, \
    RoadCategory, \
    Road, \
    CountPoint, \
    TrafficCount

from api_app.serializers import JunctionSerializer, \
    EstimationMethodSerializer, \
    RegionSerializer, \
    LocalAuthoritySerializer, \
    RoadCategorySerializer, \
    RoadSerializer, \
    CountPointSerializer, \
    TrafficCountSerializer

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

class RoadCategoryViewSet(viewsets.ModelViewSet):
    queryset = RoadCategory.objects.all()
    serializer_class = RoadCategorySerializer
    
class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer

class CountPointViewSet(viewsets.ModelViewSet):
    queryset = CountPoint.objects.all()
    serializer_class = CountPointSerializer    

class TrafficCountViewSet(viewsets.ModelViewSet):
    queryset = TrafficCount.objects.all()
    serializer_class = TrafficCountSerializer    
    
    
