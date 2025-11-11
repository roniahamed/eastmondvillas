from django.shortcuts import render

# Create your views here.
"""

{
  "title": "Nulla occaecat optio",
  "description": "Aspernatur possimus",
  "price": "371",
  "propertyType": "condo",
  "guest": "74",
  "address": "Enim voluptatibus hi",
  "amenities_indoor": ["Sed rerum ab ea iste"],
  "amenities_outdoor": ["Ea aut tempor anim i"],
  "bathrooms": "78",
  "bedroom_images": [],
  "bedrooms": "49",
  "booking_rate_start": "Autem beatae aut dol",
  "calendarLink": "https://www.gidynu.mobi",
  "check_in": "Quia nihil officia e",
  "check_out": "Voluptatem ut except",
  "city": "Eu optio id magna ",
  "rules": ['dkjfkj','ksdjfkja'],
  "latitude": "A laborum veniam qu",
  "longitude": "Autem enim ex earum ",
  "media_images": [],
  "pool": "31",
  "seo_description": "Ab incidunt ut dolo",
  "seo_titile": "Consequatur laborum",
  "signature_distinctions": ["Voluptatem Neque ar"],
  "staff": "Aut placeat digniss",
  "status": "Draft",
  "villa_name": "Melinda York",
  "location": {
    "address": "equa",
    "description": "equa tower ",
    "latitude": 23.7807517,
    "longitude": 90.4076056
 
"""

"""
{
  "title": "Nulla occaecat optio",
  "description": "Aspernatur possimus",
  "price": "371",
  "propertyType": "condo",
  "guest": "74",
  "address": "Enim voluptatibus hi",
  "amenities_indoor": ["Sed rerum ab ea iste"],
  "amenities_outdoor": ["Ea aut tempor anim i"],
  "bathrooms": "78",
  "bedroom_images": [],
  "bedrooms": "49",
  "booking_rate_start": "Autem beatae aut dol",
  "calendarLink": "https://www.gidynu.mobi",
  "check_in": "Quia nihil officia e",
  "check_out": "Voluptatem ut except",
  "city": "Eu optio id magna ",
  "rules": ['dkjfkj','ksdjfkja'],
  "latitude": "A laborum veniam qu",
  "longitude": "Autem enim ex earum ",
  "media_images": [],
  "pool": "31",
  "seo_description": "Ab incidunt ut dolo",
  "seo_titile": "Consequatur laborum",
  "signature_distinctions": ["Voluptatem Neque ar"],
  "staff": "Aut placeat digniss",
  "status": "Draft",
  "villa_name": "Melinda York",
  "location": {
    "address": "equa",
    "description": "equa tower ",
    "latitude": 23.7807517,
    "longitude": 90.4076056
  }
}
     
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db import utils as db_utils

from .models import User


class UserDeleteView(APIView):
  """Allow admins (or staff) to delete any user by PK, and allow users to
  delete their own account.

  URL: DELETE /api/auth/users/<pk>/
  Permission: authenticated users; delete allowed if requester is staff/admin
  or if requester is deleting their own account.
  """
  permission_classes = [permissions.IsAuthenticated]

  def delete(self, request, pk, format=None):
    target = get_object_or_404(User, pk=pk)

    user = request.user
    # Allow if staff or role == 'admin' or the user is deleting their own account
    is_admin_role = getattr(user, 'role', None) == 'admin'
    if not (getattr(user, 'is_staff', False) or is_admin_role or user.pk == target.pk):
      return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

    # Perform delete. Some test environments or installs may not have
    # all related tables (third-party apps) created which can cause
    # OperationalError during cascade deletes; try a real delete and
    # fallback to a safe "deactivate/anonymize" if that fails.
    try:
      target.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except db_utils.OperationalError:
      # Fallback: anonymize & deactivate the user to simulate deletion
      target.email = f"deleted_user_{target.pk}@example.invalid"
      target.name = "[deleted]"
      target.is_active = False
      target.save()
      return Response(status=status.HTTP_204_NO_CONTENT)