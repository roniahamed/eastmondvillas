# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Q

from .models import Resource
from .serializers import ResourceSerializer
from rest_framework.permissions import IsAuthenticated
from notifications.utils import create_notification_for_admin_manager_agent
from rest_framework.parsers import MultiPartParser, FormParser 




class ResourceViewSet(viewsets.ModelViewSet):
    """
    Replaces ResourceListAPIView with full CRUD support.
    Supports:
        - GET /resources/?category=branding
        - GET /resources/?search=template
        - GET /resources/?category=legal_forms&search=contract
    """
    serializer_class = ResourceSerializer
    queryset = Resource.objects.prefetch_related('media_resources').all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user

        # Restrict access
        if not user.is_authenticated or user.role not in ['admin', 'manager', 'agent']:
            return Resource.objects.none()

        queryset = Resource.objects.prefetch_related('media_resources').all().order_by('-created_at')

        category = self.request.GET.get("category")
        search = self.request.GET.get("search")

        if category:
            queryset = queryset.filter(category=category)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset

    def create(self, request, *args, **kwargs):
        # Only admin/manager can create
        if request.user.role not in ['admin', 'manager']:
            return Response({"error": "You are not permitted to add resources"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Notification
        create_notification_for_admin_manager_agent(request.user, "New Resource Added", data=serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED) 
