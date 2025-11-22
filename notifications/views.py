from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.

class NotificationList(APIView):
    def get(self, request):
        user=request.user
        if not user.is_authenticated and user.role not in ["admin", "manager", "agent"]:
            return Response({"error": "You have no permission to access this resource"}, status=status.HTTP_401_UNAUTHORIZED)
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
