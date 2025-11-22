
from django.urls import path
from .views import vila_list,ContactUsView
urlpatterns = [
    path('list/', vila_list.as_view(), name='list_vila_home'),
    path('list/<int:pk>/', vila_list.as_view(), name='list_vila_home'),
    path('contect/', ContactUsView.as_view(), name='contect_us'),
    path('contect/<int:pk>/', ContactUsView.as_view(), name='contect_us'),
]  
