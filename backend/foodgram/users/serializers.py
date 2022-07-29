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

