import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as dfilters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from users.serializers import RecipeLiteSerializer

from .filters import IngredientFilter, RecipeFilter
from .mixin import CustomGetRetrieveClass
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(CustomGetRetrieveClass):
    """Класс представления цветовых тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(CustomGetRetrieveClass):
    """Класс представления ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


def add_del_metod(request, pk, instmodel):
    user = get_object_or_404(User, username=request.user)
    recipe = get_object_or_404(Recipe, pk=pk)
    if str(request.method) == 'POST':
        instmodel.objects.get_or_create(user=user, recipe=recipe)
        recipe_serializer = RecipeLiteSerializer(recipe)
        return Response(recipe_serializer.data, status=status.HTTP_201_CREATED)
    instance = get_object_or_404(instmodel, user=user, recipe=recipe)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс представления рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (dfilters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/favorite'
    )
    def to_favorite_add_del(self, request, pk=None):
        return add_del_metod(request, pk, Favorite)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<pk>\d+)/shopping_cart'
    )
    def to_shopping_cart_add_del(self, request, pk=None):
        return add_del_metod(request, pk, ShoppingCart)

    @action(methods=['get'], detail=False, url_path='download_shopping_cart')
    def load_shop_list(self, request):
        """Функция скачивания листа покупок в файле txt."""
        user = get_object_or_404(User, username=request.user)
        recipes_id = ShoppingCart.objects.filter(user=user).values('recipe')
        recipes = Recipe.objects.filter(pk__in=recipes_id)
        shop_dict = {}
        n_rec = 0
        for recipe in recipes:
            n_rec += 1
            ing_amounts = IngredientAmount.objects.filter(recipe=recipe)
            for ing in ing_amounts:
                if ing.ingredient.name in shop_dict:
                    shop_dict[ing.ingredient.name][0] += ing.amount
                else:
                    shop_dict[ing.ingredient.name] = [
                        ing.amount,
                        ing.ingredient.measurement_unit
                    ]
        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%Y")
        shop_string = (
            f'FoodGram\nВыбрано рецептов: {n_rec}\
            \n-------------------\n{now}\
            \nСписок покупок:\
            \n-------------------'
        )
        for key, value in shop_dict.items():
            shop_string += f'\n{key} ({value[1]}) - {str(value[0])}'
        return HttpResponse(shop_string, content_type='text/plain')
