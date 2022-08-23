from api.models import Follow, Recipe
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
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


class RecipeLiteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


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
        if self.context:
            username = self.context['request'].user
            if not username.is_authenticated or obj.username == username:
                return False
            user = get_object_or_404(User, username=username)
            author = get_object_or_404(User, username=obj.username)
            return Follow.objects.filter(user=user, author=author).exists()
        return True

    def get_recipes(self, obj):
        request = self.context.get('request')
        try:
            limit = request.GET.get('recipes_limit')
        except AttributeError:
            limit = False
        author = get_object_or_404(User, username=obj.username)
        recipes = Recipe.objects.filter(author=author)
        if limit:
            recipes = recipes.all()[:int(limit)]
        return RecipeLiteSerializer(recipes, many=True).data

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
