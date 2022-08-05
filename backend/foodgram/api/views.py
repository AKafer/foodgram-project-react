from django.shortcuts import render
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, filters, status, viewsets
from .pagination import CustomPagination
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, FollowSerializer
from .models import Follow, Ingredient, Ingredient_to_Recipe, Recipe, Tag, Favorite
from users.models import User
from .mixin import MyCreateDestroyClass


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

class FavoritePostDelete(MyCreateDestroyClass):
    "Класс представления рецептов"
    queryset = Favorite.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        user = self.request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(User, pk=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            serializer.save(user=self.request.user, recipe=recipe)
    
    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        follow = Follow.objects.filter(user=user, author=author).first()
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
