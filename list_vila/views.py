from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.shortcuts import get_object_or_404
from .models import VilaListing,ContectUs
from .serializers import VilaListingSerializer,ContectUsSerializer
from notifications.utils import notify_admins_and_managers

# Create your views here.


class vila_list(APIView):
    def get(self, request,pk=None):
        if request.user.role == "admin" or request.user.is_superuser:
            if pk:
                vila = get_object_or_404(VilaListing,pk=pk)
                serializer = VilaListingSerializer(vila)
                return Response(serializer.data)
            vila = VilaListing.objects.all()
            serializer = VilaListingSerializer(vila, many=True)
            return Response(serializer.data)
        return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    def post(self,request):
        data = request.data
        serializer = VilaListingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            notify_admins_and_managers("New Vila Listing", data=serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        if request.user.role == "admin" or request.user.is_superuser:
            vila = get_object_or_404(VilaListing,pk=pk)
            serializer = VilaListingSerializer(vila, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    def delete(self, request, pk):
        if request.user.role == "admin" or request.user.is_superuser:
            vila = get_object_or_404(VilaListing,pk=pk)
            vila.delete()
            return Response({"message": "Vila deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    

from accounts.permissions import IsAdminOrManager

class ContactUsView(APIView):

    def get_permissions(self):
        # POST → open for everyone
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        
        # GET, PUT, DELETE → only admin or manager
        return [IsAdminOrManager()]

    # GET all or single
    def get(self, request, pk=None):
        if pk:
            contact = get_object_or_404(ContectUs, pk=pk)
            serializer = ContectUsSerializer(contact)
            return Response(serializer.data)

        contacts = ContectUs.objects.all()
        serializer = ContectUsSerializer(contacts, many=True)
        return Response(serializer.data)

    # POST (anyone can submit)
    def post(self, request):
        serializer = ContectUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            notify_admins_and_managers(
                "New Contact Us", 
                data=serializer.data
            )
            

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE
    def put(self, request, pk):
        contact = get_object_or_404(ContectUs, pk=pk)
        serializer = ContectUsSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, pk):
        contact = get_object_or_404(ContectUs, pk=pk)
        contact.delete()
        return Response(
            {"message": "Contact deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )