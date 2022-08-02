from io import BytesIO
import base64
from PIL import Image
from rest_framework import serializers
from .models import Ingredient, Recipe, Tag


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

class RecipeSerializer(serializers.ModelSerializer):
    image = ImageConversion()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                 'tags', 'cooking_time')

