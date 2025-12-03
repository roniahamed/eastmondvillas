from django.urls import path, include
from faqs.views import FAQViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]