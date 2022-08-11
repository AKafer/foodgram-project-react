import base64

from api.models import Follow, Recipe
from django.shortcuts import get_object_or_404
from djoser.compat import get_user_email_field_name
from djoser.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class MyUserCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатора для djoser для создания пользователей."""

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )


class MyUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для djoser для управления пользователями."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Функция определения подписан ли текущий пользователь на автора"""
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return False


class MyUserSubsSerializer(serializers.ModelSerializer):
    """Класс сериализатора djoser для управления авторами
    с дополтнительными полями: подписан ли текущий юзер, рецептами автора,
    числом рецептов."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_is_subscribed(self, obj):
        """Функция определения подписан ли текущий пользователь на автора"""
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return True

    def get_recipes(self, obj):
        """Функция получения рецептов автора"""
        author = get_object_or_404(User, username=obj.username)
        recipes = Recipe.objects.filter(author=author)
        list_rec = []
        for recipe in recipes:
            encoded_string = base64.b64encode(recipe.image.read())
            code_image = 'data:image/jpeg;base64,' + encoded_string.decode()
            list_rec.append({
                "id": recipe.id,
                "name": recipe.name,
                "image": code_image,
                "cooking_time": recipe.cooking_time
            })
        return list_rec[:3]

    def get_recipes_count(self, obj):
        """Функция подсчета числа рецептов автора"""
        author = get_object_or_404(User, username=obj.username)
        return Recipe.objects.filter(author=author).count()


class MyTokenCreateSerializer(serializers.Serializer):
    """Кастомный класс для djoser для выдачи токенов по email и password"""
    password = serializers.CharField(
        required=False,
        style={"input_type": "password"})

    default_error_messages = {
        "invalid_credentials": settings.
        CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.
        CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
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
                return self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            return attrs
        return self.fail("inactive_account")


class FollowSerializer(serializers.ModelSerializer):
    """Класс сериализатора для Follow."""

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Эей, такая запись уже есть'
            )
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Не спи! Нельзя подписываться на самого себя')
        return data
