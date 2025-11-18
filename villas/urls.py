from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, BookingViewSet, get_property_availability


router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'bookings', BookingViewSet, basename='booking')



urlpatterns = [
    path('', include(router.urls)),
    path('properties/<int:property_pk>/availability/', get_property_availability, name='property-availability'
),
]