from email.policy import default
from rest_framework import serializers
from .models import User 


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'password'
        )

class UserMeSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    is_subscribed=serializers.CharField(default=False)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

class TokenGeneratorSerialiser(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'email', 'password'
        )

