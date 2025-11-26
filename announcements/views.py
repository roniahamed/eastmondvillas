# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Announcement, FileUpload
from .serializers import AnnouncementSerializer
from accounts.permissions import IsAdminOrManager, IsAgentOrAdminOrManager
from notifications.utils import create_notification_for_customers


class AnnouncementListCreateAPIView(APIView):
    
    parser_classes = [MultiPartParser, FormParser]  
    
    permission_classes = [IsAgentOrAdminOrManager] 
    
    def get(self, request):
        announcements = Announcement.objects.all().order_by('-created_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        announcement = Announcement.objects.create(**serializer.validated_data)

        files = request.FILES.getlist('files')  

        for f in files:
            FileUpload.objects.create(
                announcement=announcement,
                file=f
            )

        out_serializer = AnnouncementSerializer(announcement)
        create_notification_for_customers(request.user,title="New Announcement", data=out_serializer.data)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
