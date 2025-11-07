from rest_framework import viewsets, permissions
from .models import Villa, Booking, Amenity, VillaImage
from .serializers import VillaSerializer, BookingSerializer, AmenitySerializer, VillaImageSerializer
from .permissions import IsAdminAgentManager, IsBookingOwnerOrManager


class VillaViewSet(viewsets.ModelViewSet):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer

    def get_permissions(self):
        # list/retrieve: public
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        # create/update/delete: only admin/manager/agent
        return [IsAdminAgentManager()]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        # create: any authenticated user (customer can create)
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        # list: managers/admin can view all; customers only their own (DRF filtering should be added separately)
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsBookingOwnerOrManager()]
        # default to authenticated
        return [permissions.IsAuthenticated()]


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]


class VillaImageViewSet(viewsets.ModelViewSet):
    queryset = VillaImage.objects.all()
    serializer_class = VillaImageSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdminAgentManager()]
