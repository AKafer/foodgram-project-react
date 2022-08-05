from io import BytesIO
import base64
from django.shortcuts import get_object_or_404
#from PIL import Image
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from .models import Follow, Ingredient, Ingredient_to_Recipe, Recipe, Tag, Tag_to_Recipe
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

class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатора ингридиентов."""

    class Meta:
        model = Ingredient_to_Recipe
        fields = ('id', 'amount')


    def get_amount(self, obj):

        print('ВНИМАНИЕ')
        print('ЗАПРОС', self)

        ing_to = get_object_or_404(Ingredient_to_Recipe, ingredient=obj)



        return ing_to.amount
    

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    #author = serializers.SlugRelatedField(quiryset=User.objects.all(), slug_field='recipes')
    #author = serializers.PrimaryKeyRelatedField(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True)
    #ingredients = serializers.SerializerMethodField()
    #ingredients = serializers.SlugRelatedField(quiryset=Ingredient_to_Recipe.objects.all(), slug_field='ing')
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
        validated_data.pop('ingredients')
        #validated_data.pop('ingredients')
        print(tag_list)
        print(ing_list)
        print(validated_data)
        recipe = Recipe.objects.create(**validated_data)

        for tag_pk in tag_list:
            cur_tag = get_object_or_404(Tag, pk=tag_pk)
            Tag_to_Recipe.objects.create(tag=cur_tag, recipe=recipe)

        print('Я ЗДЕСЬ')
        for ing in ing_list:
            cur_ing = get_object_or_404(Ingredient, pk=ing['id'])

            recipe.ingredients.add(cur_ing)

            """cur_ing = get_object_or_404(Ingredient, pk=ing['id'])
            Ingredient_to_Recipe.objects.create(
                ingredient=cur_ing,
                amount=ing['amount']
            )"""

        print("ТУТ ЗАКОНЧИЛИ")
        return recipe

    def get_ingredients(self, obj):
        print("ДАННЫЕ ЗДЕСЬ")
        print(obj)
        print(obj.tags)
        print(obj.cooking_time)
        print(obj.author)
        print(obj.ingredients)
        return

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'author')

        """ validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Подписка уже существует!',
            )
        ]

    def validate_author(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return value"""