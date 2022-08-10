from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import MyUserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, TagRecipe)


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
    """Класс сериализатора ингредиентов в рецепте"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Класс сериализатора рецептов"""
    image = Base64ImageField()
    author = MyUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients',
                  'tags', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def create(self, validated_data):
        tag_list = self.initial_data.pop('tags')
        ing_list = self.initial_data.pop('ingredients')
        print(ing_list)
        recipe = Recipe.objects.create(**validated_data)
        for tag_pk in tag_list:
            cur_tag = get_object_or_404(Tag, pk=tag_pk)
            TagRecipe.objects.create(tag=cur_tag, recipe=recipe)
        for ing in ing_list:
            cur_ing = get_object_or_404(Ingredient, pk=ing['id'])
            IngredientAmount.objects.create(
                ingredient=cur_ing,
                recipe=recipe,
                amount=ing['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        print(self.initial_data)
        tag_list = self.initial_data.pop('tags')
        ing_list = self.initial_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientAmount.objects.filter(recipe=instance).delete()
        for tag_pk in tag_list:
            cur_tag = get_object_or_404(Tag, pk=tag_pk)
            TagRecipe.objects.create(tag=cur_tag, recipe=instance)
        for ing in ing_list:
            cur_ing = get_object_or_404(Ingredient, pk=ing['id'])
            IngredientAmount.objects.create(
                ingredient=cur_ing,
                recipe=instance,
                amount=ing['amount']
            )
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        """Функция проверки добавления текущим пользователем
        рецепта в избранное."""
        try:
            user_username = self.context['view'].request.user
            user = get_object_or_404(User, username=user_username)
        except Exception:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Функция проверки добавления текущим пользователем
        рецепта в лист покупок."""
        try:
            user_username = self.context['view'].request.user
            user = get_object_or_404(User, username=user_username)
        except Exception:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
