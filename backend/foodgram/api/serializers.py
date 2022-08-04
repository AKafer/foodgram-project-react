from io import BytesIO
import base64
from django.shortcuts import get_object_or_404
#from PIL import Image
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Ingredient, Ingredient_to_Recipe, Recipe, Tag, Tag_to_Recipe
from users.serializers import MyUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """Класс сериализатора тэгов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')

class TagRecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатора тэгов."""
    class Meta:
        model = Tag
        fields = ('id')

class IngredientSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')

class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""
    ingredient = IngredientSerializer()

    class Meta:
        model = Ingredient
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                 'tags', 'cooking_time')
        read_only_fields = ('author',)
  
    def create(self, validated_data):
        print('НАЧАЛО ДАННЫХ')
        print(self.initial_data)
        print('КОНЕЦ ДАННЫХ')
        tag_list = self.initial_data.pop('tags')
        ing_list = self.initial_data.pop('ingredients')
        #validated_data.pop('ingredients')
        print(tag_list)
        print(ing_list)
        recipe = Recipe.objects.create(**validated_data)

        for tag_pk in tag_list:
            cur_tag = get_object_or_404(Tag, pk=tag_pk)
            Tag_to_Recipe.objects.create(tag=cur_tag, recipe=recipe)

        for ing in ing_list:
            cur_ing = get_object_or_404(Ingredient, pk=ing['id'])
            Ingredient_to_Recipe.objects.create(
                ingredient=cur_ing,
                recipe=recipe,
                amount=ing['amount']
            )
        print("ТУТ ЗАКОНЧИЛИ")
        return recipe
        

