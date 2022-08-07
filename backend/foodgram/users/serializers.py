from email.policy import default
import base64
from django.core import serializers as sz
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import User 
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
#from api.serializers import RecipeSerializer
from django.utils.translation import gettext_lazy as _
from api.models import Follow, Recipe
from djoser.compat import get_user_email_field_name
from djoser.conf import settings


class MyUserCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password'
        )


class MyUserSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )
    
    def get_is_subscribed(self, obj):
        try:
            user_username = self.context['view'].request.user
            user = get_object_or_404(User, username=user_username)
        except:
            return False
        if obj.username == user_username:
            return False
        author = get_object_or_404(User, username=obj.username)
        return Follow.objects.filter(user=user, author=author).exists()


class MyUserSubsSerializer(serializers.ModelSerializer):
    """Класс сериализатора пользователей для админа."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('email', 'username', 'first_name','last_name')
    
    def get_is_subscribed(self, obj):
        try:
            user_username = self.context['view'].request.user
            user = get_object_or_404(User, username=user_username)
        except:
            return True
        if obj.username == user_username:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()
    
    def get_recipes(self, obj):
        author = get_object_or_404(User, username=obj.username)
        recipes = Recipe.objects.filter(author=author)
        #recipes =recipes.values('id', 'name', 'image', 'cooking_time')
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
        return list_rec[0:3]
    
    def get_recipes_count(self, obj):
        author = get_object_or_404(User, username=obj.username)
        number_recipes = Recipe.objects.filter(author=author).count()
        return number_recipes

   
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


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'author')
