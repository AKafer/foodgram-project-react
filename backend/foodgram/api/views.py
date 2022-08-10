import base64

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as dfilters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .filters import MyIngredientFilter, MyRecipeFilter
from .mixin import CustomGetRetrieveClass
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import OwnerOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(CustomGetRetrieveClass):
    """Класс представления цветовых тэгов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(CustomGetRetrieveClass):
    """Класс представления ингридиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = MyIngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс представления рецептов"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = MyRecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/favorite'
    )
    def subs_add_del(self, request, pk=None):
        """Функция добавления и удаления рецептов в избранное"""
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
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

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/shopping_cart'
    )
    def shopping_cart_add_del(self, request, pk=None):
        """Фукция добавления и удаления рецептов в лист покупок"""
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, pk=pk)
        if str(self.request.method) == 'POST':
            ShoppingCart.objects.get_or_create(user=user, recipe=recipe)
            encoded_string = base64.b64encode(recipe.image.read())
            code_image = 'data:image/jpeg;base64,' + encoded_string.decode()
            recipe_responce = {
                "id": recipe.id,
                "name": recipe.name,
                "image": code_image,
                "cooking_time": recipe.cooking_time
            }
            return Response(recipe_responce, status=status.HTTP_201_CREATED)
        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart')
    def load_shop_list(self, request):
        """Функция скачивания листа покупок в файле txt"""
        user = get_object_or_404(User, username=request.user)
        recipes_id = ShoppingCart.objects.filter(user=user).values('recipe')
        recipes = Recipe.objects.filter(pk__in=recipes_id)
        shop_dict = {}
        for recipe in recipes:
            ing_amounts = IngredientAmount.objects.filter(recipe=recipe)
            n_rec = 0
            for ing in ing_amounts:
                n_rec += 1
                if ing.ingredient.name in shop_dict:
                    shop_dict[ing.ingredient][0] += ing.amount
                else:
                    shop_dict[ing.ingredient.name] = [
                        ing.amount,
                        ing.ingredient.measurement_unit
                    ]
        shop_string = 'Food_gram\nВыбрано рецпетов: {n_rec}\nСписок покупок:'
        for key, value in shop_dict.items():
            shop_string += f'\n{key} ({value[1]}) - {str(value[0])}'
        return HttpResponse(shop_string, content_type='text/plain')
