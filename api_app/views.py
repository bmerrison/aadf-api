from rest_framework import viewsets

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

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

class RoadCategoryViewSet(viewsets.ModelViewSet):
    queryset = RoadCategory.objects.all()
    serializer_class = RoadCategorySerializer
    
class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer

class CountPointViewSet(viewsets.ModelViewSet):
    queryset = CountPoint.objects.all()
    serializer_class = CountPointSerializer    

    def get_queryset(self):
        queryset = CountPoint.objects.all()

        # Optional simple filter criteria. If multiple criteria are given,
        # the results must match them all.
        possible_filters = (('reference', 'reference'),
                            ('road', 'road'),
                            ('road_name', 'road__name'),
                            ('ward', 'ward'),
                            ('ward_name', 'ward__name'),
                            ('local_authority', 'local_authority'),
                            ('local_authority_name', 'local_authority__name'),
                            ('start_junction', 'start_junction'),
                            ('start_junction_desc', 'start_junction__description'),
                            ('end_junction', 'end_junction'),
                            ('end_junction_desc', 'end_junction__description'),)
        kwargs = {}
        for req_param, attrib in possible_filters:
            req_val = self.request.query_params.get(req_param, None)
            if req_val is not None:
                kwargs[attrib] = req_val
        queryset = queryset.filter(**kwargs)

        # Optional criteria that can be used to retrieve count points in
        # a given rectangle.
        if 'min_northing' in self.request.query_params:
            queryset = queryset.filter(northing__gte=self.request.query_params['min_northing'])
        if 'max_northing' in self.request.query_params:
            queryset = queryset.filter(northing__lte=self.request.query_params['max_northing'])
        if 'min_easting' in self.request.query_params:
            queryset = queryset.filter(easting__gte=self.request.query_params['min_easting'])
        if 'max_easting' in self.request.query_params:
            queryset = queryset.filter(easting__lte=self.request.query_params['max_easting'])
            
        return queryset
    
class TrafficCountViewSet(viewsets.ModelViewSet):
    serializer_class = TrafficCountSerializer    
    
    def get_queryset(self):
        queryset = TrafficCount.objects.all()

        # Optional simple filter criteria. If multiple criteria are given,
        # the results must match them all.
        possible_filters = (('count_point', 'count_point'),
                            ('count_point_ref', 'count_point__reference'),
                            ('year', 'year'),
                            ('estimated', 'estimated'),
                            ('road', 'count_point__road'),
                            ('road_name', 'count_point__road__name'),
                            ('ward', 'count_point__ward'),
                            ('ward_name', 'count_point__ward__name'),
                            ('local_authority', 'count_point__local_authority'),
                            ('local_authority_name', 'count_point__local_authority__name'),
                            ('start_junction', 'count_point__start_junction'),
                            ('start_junction_desc', 'count_point__start_junction__description'),
                            ('end_junction', 'count_point__end_junction'),
                            ('end_junction_desc', 'count_point__end_junction__description'),)
        kwargs = {}
        for req_param, attrib in possible_filters:
            req_val = self.request.query_params.get(req_param, None)
            if req_val is not None:
                kwargs[attrib] = req_val
        queryset = queryset.filter(**kwargs)

        return queryset
