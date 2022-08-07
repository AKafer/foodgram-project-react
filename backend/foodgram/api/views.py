from django.shortcuts import render
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, filters, status, viewsets
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, FavoriteSerializer
from .models import Follow, Ingredient, Recipe, Tag, Favorite
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

class RecipeViewSet(viewsets.ModelViewSet):
    "Класс представления рецептов"
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',) 


    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

class FavoritePostDelete(viewsets.ModelViewSet):
    "Класс представления рецептов"
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, username = self.request.user)
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            serializer.save(user=user, recipe=recipe)
    
    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
