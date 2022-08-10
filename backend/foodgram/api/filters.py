from django.shortcuts import get_object_or_404
from django_filters import rest_framework as dfilters

from .models import Favorite, Ingredient, Recipe, ShoppingCart, User


class MyIngredientFilter(dfilters.FilterSet):
    """Фильтр для поиска ингредиентов по имени"""
    name = dfilters.CharFilter(field_name="name", lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ('name', )


class MyRecipeFilter(dfilters.FilterSet):
    """Фильтр рецептов по полям: автор, тэги, избранное, в корзине покупок"""
    author = dfilters.CharFilter()
    is_favorited = dfilters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = dfilters.BooleanFilter(
        method='get_is_in_shopping_cart')
    tags = dfilters.AllValuesMultipleFilter(
        field_name="tags__slug", lookup_expr="icontains")

    def get_is_favorited(self, queryset, name, value):
        """Функция фильтрации рецептов по избранному и тэгам."""
        list_tags = self.request.query_params.getlist('tags')
        user = get_object_or_404(User, username=self.request.user)
        favorite_recipes = Favorite.objects.filter(user=user).values('recipe')
        if list_tags:
            queryset = Recipe.objects.filter(
                pk__in=favorite_recipes, tags__slug__in=list_tags).distinct()
        else:
            queryset = Recipe.objects.filter(pk__in=favorite_recipes)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        """Функция фильрации рецептов по добавлению в корзину покупок"""
        user = get_object_or_404(User, username=self.request.user)
        for_shopping_recipes = ShoppingCart.objects.filter(
            user=user).values('recipe')
        queryset = Recipe.objects.filter(pk__in=for_shopping_recipes)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', )
