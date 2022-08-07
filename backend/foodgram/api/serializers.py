from io import BytesIO
import base64
from django.shortcuts import get_object_or_404
#from PIL import Image
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Follow, Ingredient, Recipe, Tag, Tag_to_Recipe, IngredientAmount, Favorite
from rest_framework.validators import UniqueTogetherValidator


from users.serializers import MyUserSerializer
from users.models import User

class TagSerializer(serializers.ModelSerializer):
    """Класс сериализатора тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

class IngredientSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class IngredientAmountSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""
    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
    

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                 'tags', 'cooking_time', 'is_favorited')
        #read_only_fields = ('author',)
  
    def create(self, validated_data):
        tag_list = self.initial_data.pop('tags')
        ing_list = self.initial_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag_pk in tag_list:
            print(tag_pk)
            cur_tag = get_object_or_404(Tag, pk=tag_pk)
            Tag_to_Recipe.objects.create(tag=cur_tag, recipe=recipe)
        for ing in ing_list:
            cur_ing = get_object_or_404(Ingredient, pk=ing['id'])
            IngredientAmount.objects.create(
                name = cur_ing.name,
                measurement_unit=cur_ing.measurement_unit,
                recipe=recipe,
                amount=ing['amount']  
            )
        return recipe

    def get_is_favorited(self, obj):
        try:
            user_username = self.context['view'].request.user
            user = get_object_or_404(User, username=user_username)
        except:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    """Класс сериализатора тэгов."""
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')
        read_only_fields = ('user', 'recipe')
