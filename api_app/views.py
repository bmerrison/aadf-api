from rest_framework import viewsets

from api_app.models import Junction
from api_app.serializers import JunctionSerializer

class JunctionViewSet(viewsets.ModelViewSet):
    queryset = Junction.objects.all()
    serializer_class = JunctionSerializer
    
