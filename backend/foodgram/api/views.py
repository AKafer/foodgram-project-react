from django.shortcuts import render
import base64
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django_filters import rest_framework as dfilters
from rest_framework import mixins, filters, status, viewsets
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, FavoriteSerializer
from .models import Follow, Ingredient, Recipe, Tag, Favorite
from users.models import User
from .mixin import MyCreateDestroyClass
from .filters import MyFilter


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
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = MyFilter


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(methods=['post', 'delete'], detail=False, url_path=r'(?P<id>\d+)/favorite')
    def subs_add_del(self, request, id=None):
        user = get_object_or_404(User, username = request.user)
        recipe = get_object_or_404(Recipe, pk=id)
        if str(self.request.method) == 'POST':
            Favorite.objects.get_or_create(user=user, recipe=recipe)
            encoded_string = base64.b64encode(recipe.image.read())
            code_image = 'data:image/jpeg;base64,' + encoded_string.decode()
            recipe_responce = {
                "id": recipe.id,
                "name": recipe.name,
                "image": code_image,
                "cooking_time": recipe.cooking_time
            }
            return Response(recipe_responce, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        

    """@action(methods=['post'], detail=False, url_path=r'(?P<id>\d+)/favorite')
    def new_create(self, request, id=None):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        user = get_object_or_404(User, username = request.user)
        print(user)
        recipe = get_object_or_404(Recipe, pk=id)
        Favorite.objects.get_or_create(user=user, recipe=recipe)
        encoded_string = base64.b64encode(recipe.image.read())
        code_image = 'data:image/jpeg;base64,' + encoded_string.decode()
        recipe_responce = {
            "id": recipe.id,
            "name": recipe.name,
            "image": code_image,
            "cooking_time": recipe.cooking_time
        }
        return Response(recipe_responce, status=status.HTTP_200_OK)


    @action(methods=['delete'], detail=False, url_path=r'(?P<id>\d+)/favorite')
    def new_create(self, request, id=None):
        user = get_object_or_404(User, username = request.user)
        recipe = get_object_or_404(Recipe, pk=id)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


"""class FavoritePostDelete(viewsets.ModelViewSet):
    "Класс представления рецептов"
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, username = self.request.user)
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            serializer.save(user=user, recipe=recipe)
    
    @action(methods=['post'], detail=False)
    def new_create(self, request, **kwargs):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        user = get_object_or_404(User, username = request.user)
        print(user)
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            serializer = FavoriteSerializer()
            serializer.save(user=user, recipe=recipe)
            #return Response(recipe.values('id', 'name', 'image', 'cooking_time') , status=status.HTTP_201_CREATED)


    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)""" 
