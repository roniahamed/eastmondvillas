from django.urls import path
from .views import NotificationList

urlpatterns = [
    path("list/", NotificationList.as_view(), name="notification-list"),
]