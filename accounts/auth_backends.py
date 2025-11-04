from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError 

from django.db.models import Q 


User = get_user_model() 


class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if not user.is_active:
            raise ValidationError("This account is inactive. Please Contact with support!")
        return super().user_can_authentication(user)
    
