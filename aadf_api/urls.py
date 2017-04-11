"""aadf_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from api_app import views

class Router(DefaultRouter):
    def get_api_root_view(self, api_urls=None):
        root_view = super(Router, self).get_api_root_view(api_urls=api_urls)
        root_view.cls.__doc__ = "Welcome to the browsable annual average daily flow API. Click one of the links below to view objects. These aren't filtered, so opening a link with a lot of entries (e.g. traffic counts) might be very slow!"
        return root_view

router = Router()

#router = DefaultRouter()
router.register(r'junctions', views.JunctionViewSet)
router.register(r'estimation_methods', views.EstimationMethodViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'local_authorities', views.LocalAuthorityViewSet)
router.register(r'wards', views.WardViewSet)
router.register(r'road_categories', views.RoadCategoryViewSet)
router.register(r'roads', views.RoadViewSet)
router.register(r'count_points', views.CountPointViewSet)
router.register(r'traffic_counts', views.TrafficCountViewSet,
                base_name='trafficcounts')

schema_view = get_schema_view(title='Average Annual Daily Flow API')

urlpatterns = [
    url(r'^docs/', include_docs_urls(title='Average Annual Daily Flow API')),
    url(r'^schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^', include(router.urls))
]
