from io import BytesIO
import base64
from django.shortcuts import get_object_or_404
#from PIL import Image
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Ingredient, Ingredient_to_Recipe, Recipe, Tag
from users.serializers import MyUserSerializer



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

class IngredientPOSTSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')

"""
class Ingredient_to_RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Ingredient_to_Recipe
        fields = ('ingredients', 'amount')
"""
"""

class ImageConversion(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            with open(data, "rb") as image_file:
                image = base64.b64encode(image_file.read())
        except ValueError:
            raise serializers.ValidationError(
                'Не вышло декодировать картинку'
            )
        return image

"""

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                 'tags', 'cooking_time')
        read_only_fields = ('author',)
    
    
    def create(self, validated_data):
        # Уберем список достижений из словаря validated_data и сохраним его
        ing_list = self.initial_data.pop('ingredients')

        # Создадим нового котика пока без достижений, данных нам достаточно
        recipe = Recipe.objects.create(**validated_data)
    
        # Для каждого достижения из списка достижений
        for ing in ing_list:
            # Создадим новую запись или получим существующий экземпляр из БД
            #current_ingredient = get_object_or_404(Ingredient, id=ingredient['id'])
            

            # Не забыв указать к какому котику оно относится
            Ingredient_to_Recipe.objects.create(
                ingredients=ing['id'],
                recipe = recipe,
                amount = ing['amount']
            )
           
        return recipe
        

