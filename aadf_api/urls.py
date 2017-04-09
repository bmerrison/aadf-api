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
from api_app import views

router = DefaultRouter()
router.register(r'junctions', views.JunctionViewSet)
router.register(r'estimation_methods', views.EstimationMethodViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'local_authorities', views.LocalAuthorityViewSet)
schema_view = get_schema_view(title='Average Annual Daily Flow API')

urlpatterns = [
    url(r'^schema/$', schema_view),
    url(r'^', include(router.urls))
]
