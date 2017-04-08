from rest_framework import viewsets

from api_app.models import Junction, EstimationMethod
from api_app.serializers import JunctionSerializer, EstimationMethodSerializer

class JunctionViewSet(viewsets.ModelViewSet):
    queryset = Junction.objects.all()
    serializer_class = JunctionSerializer

class EstimationMethodViewSet(viewsets.ModelViewSet):
    queryset = EstimationMethod.objects.all()
    serializer_class = EstimationMethodSerializer
    
