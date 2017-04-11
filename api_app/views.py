from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

import django_filters

from api_app.models import Junction, \
    EstimationMethod, \
    Region, \
    LocalAuthority, \
    Ward, \
    RoadCategory, \
    Road, \
    CountPoint, \
    TrafficCount

from api_app.serializers import JunctionSerializer, \
    EstimationMethodSerializer, \
    RegionSerializer, \
    LocalAuthoritySerializer, \
    WardSerializer, \
    RoadCategorySerializer, \
    RoadSerializer, \
    CountPointSerializer, \
    TrafficCountSerializer

class JunctionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Junction.objects.all()
    serializer_class = JunctionSerializer

class EstimationMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstimationMethod.objects.all()
    serializer_class = EstimationMethodSerializer
    
class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class LocalAuthorityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LocalAuthority.objects.all()
    serializer_class = LocalAuthoritySerializer

class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

class RoadCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RoadCategory.objects.all()
    serializer_class = RoadCategorySerializer
    
class RoadViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer

class CountPointFilter(FilterSet):
    road_name = django_filters.CharFilter(name='road__name')
    ward_name = django_filters.CharFilter(name='ward__name')
    local_authority = django_filters.NumberFilter(name='ward__local_authority')
    local_authority_name = django_filters.CharFilter(name='ward__local_authority__name')
    start_junction_desc = django_filters.CharFilter(name='start_junction__description')
    end_junction_desc = django_filters.CharFilter(name='end_junction__description')
    min_easting = django_filters.NumberFilter(name='easting', lookup_expr='gte')
    max_easting = django_filters.NumberFilter(name='easting', lookup_expr='lte')
    min_northing = django_filters.NumberFilter(name='northing', lookup_expr='gte')
    max_northing = django_filters.NumberFilter(name='northing', lookup_expr='lte')    
    class Meta:
        model = CountPoint
        fields = ['reference', 'road', 'road_name', 'ward', 'start_junction',
                  'start_junction_desc', 'end_junction', 'end_junction_desc',
                  'min_easting', 'max_easting', 'min_northing', 'max_northing']
        
class CountPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Returns a list of count points. The optional parameters given below
    can be used to filter the list. For example, the min_ and max_ northing and
    easting parameters can be used to find all count points in a particular
    rectangular area. Instances are returned that match all of the specified criteria.
    Note that the 'page' parameter is currently ignored.
    read: Returns one count point instance, using its ID. Note that this should
    be a database ID (i.e. as returned form the 'list' action), not its count 
    point reference (the value given in the CSV data). 
    """
    queryset = CountPoint.objects.all()
    serializer_class = CountPointSerializer    
    filter_backends = (DjangoFilterBackend,)
    filter_class = CountPointFilter

class TrafficCountFilter(FilterSet):
    count_point_reference = django_filters.NumberFilter(name='count_point__reference')
    road = django_filters.NumberFilter(name='count_point__road')
    road_name = django_filters.CharFilter(name='count_point__road__name')
    ward = django_filters.NumberFilter(name='count_point__ward')
    ward_name = django_filters.CharFilter(name='count_point__ward__name')
    local_authority = django_filters.NumberFilter(name='count_point__ward__local_authority')
    local_authority_name = django_filters.CharFilter(name='count_point__ward__local_authority__name')
    start_junction = django_filters.NumberFilter(name='count_point__start_junction')
    start_junction_desc = django_filters.CharFilter(name='count_point__start_junction__description')
    end_junction = django_filters.NumberFilter(name='count_point__end_junction')
    end_junction_desc = django_filters.CharFilter(name='count_point__end_junction__description')
    min_easting = django_filters.NumberFilter(name='count_point__easting', lookup_expr='gte')
    max_easting = django_filters.NumberFilter(name='count_point__easting', lookup_expr='lte')
    min_northing = django_filters.NumberFilter(name='count_point__northing', lookup_expr='gte')
    max_northing = django_filters.NumberFilter(name='count_point__northing', lookup_expr='lte')    
    class Meta:
        model = TrafficCount
        fields = ['count_point_reference', 'road', 'road_name', 'ward', 'start_junction',
                  'start_junction_desc', 'end_junction', 'end_junction_desc',
                  'min_easting', 'max_easting', 'min_northing', 'max_northing', 'year', 'estimated']
    
class TrafficCountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Returns a list of traffic counts. The optional parameters given below
    can be used to filter the list. For example, the ward_name and year parameters
    can be used to find all counts in a particular ward in a given year.
    Instances are returned that match all of the specified criteria. Note that the 'page'
    parameter is currently ignored.
    read: Returns one count instance, using its database ID (i.e. as returned by the list action).
    """
    queryset = TrafficCount.objects.all()
    serializer_class = TrafficCountSerializer    
    filter_backends = (DjangoFilterBackend,)
    filter_class = TrafficCountFilter
    
