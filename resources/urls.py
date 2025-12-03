from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register(r'', ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(routers.urls)),
]
