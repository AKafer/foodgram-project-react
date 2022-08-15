import base64

from api.models import Follow, Recipe
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class MyUserCreateSerializer(UserCreateSerializer):
    """Класс сериализатора для djoser для создания пользователей."""

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password'
        )


class MyUserSerializer(UserSerializer):
    """Класс сериализатора для djoser для управления пользователями."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Функция определения подписан ли текущий пользователь на автора."""
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return False


class MyUserSubsSerializer(UserSerializer):
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
        """Функция определения подписан ли текущий пользователь на автора."""
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


class FollowSerializer(serializers.ModelSerializer):
    """Класс сериализатора для управления подписками."""

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
