from django.urls import path
from .views import AnnouncementListCreateAPIView

urlpatterns = [
    path('announcement/', AnnouncementListCreateAPIView.as_view(), name='announcementViews'),
]   