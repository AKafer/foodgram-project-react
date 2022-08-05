from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from .pagination import CustomPagination
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, FollowSerializer
from .models import Follow, Ingredient, Ingredient_to_Recipe, Recipe, Tag
from users.models import User


class TagViewSet(viewsets.ModelViewSet):
    "Класс представления цветовых тэгов"
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    "Класс представления ингридиентов"
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

"""
class Ingredient_to_RecipeViewSet(viewsets.ModelViewSet):
    "Класс представления ингридиентов"
    queryset =Ingredient_to_Recipe.objects.all()
    serializer_class = Ingredient_to_RecipeSerializer
"""

class RecipeViewSet(viewsets.ModelViewSet):
    "Класс представления рецептов"
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 
