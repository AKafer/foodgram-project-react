from django_filters import rest_framework as dfilters
from django.shortcuts import get_object_or_404
from django_filters.fields import CSVWidget

from .models import Recipe, Favorite, User, ShoppingCart


class CharFilterInFilter(dfilters.BaseInFilter, dfilters.CharFilter):
    pass

class MyFilter(dfilters.FilterSet):
    author = dfilters.CharFilter()
    is_favorited = dfilters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = dfilters.BooleanFilter(method='get_is_in_shopping_cart')
    tags = dfilters.AllValuesMultipleFilter(field_name = "tags__slug", lookup_expr="icontains")
    

    def get_is_favorited(self, queryset, name, value):
        user = get_object_or_404(User, username=self.request.user)
        favorite_recipes=Favorite.objects.filter(user=user).values('recipe')
        queryset = Recipe.objects.filter(pk__in=favorite_recipes)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = get_object_or_404(User, username=self.request.user)
        for_shopping_recipes = ShoppingCart.objects.filter(user=user).values('recipe')
        queryset = Recipe.objects.filter(pk__in=for_shopping_recipes)
        return queryset
    
    """def get_tags(self, queryset, name, values):
        print(values)
        print(self.request)
        print(self.request.url)
        return queryset.filter(tags__slug__in=values)"""

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)