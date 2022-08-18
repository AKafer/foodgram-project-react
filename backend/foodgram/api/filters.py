from django_filters import rest_framework as dfilters

from .models import Ingredient, Recipe, Tag


class IngredientFilter(dfilters.FilterSet):
    """Фильтр для поиска ингредиентов по имени"""
    name = dfilters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(dfilters.FilterSet):
    """Фильтр рецептов по полям: автор, тэги, избранное, в корзине покупок"""
    author = dfilters.CharFilter()
    is_favorited = dfilters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = dfilters.BooleanFilter(
        method='get_is_in_shopping_cart')
    tags = dfilters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', )
