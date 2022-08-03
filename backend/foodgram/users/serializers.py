from email.policy import default
from rest_framework import serializers
from .models import User 
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from djoser.compat import get_user_email_field_name
from djoser.conf import settings



class MyUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name'
        )

class MyUserCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )

class MyTokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={"input_type": "password"})

    
    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        self.user = User.objects.filter(email=email, password=password).first()
        if not self.user:
            self.user = User.objects.filter(email=email).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        self.fail("inactive_account")
    
