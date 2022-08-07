from django_filters import rest_framework as dfilters
from django.shortcuts import get_object_or_404
from django_filters.fields import CSVWidget

from .models import Recipe, Favorite, User


class CharFilterInFilter(dfilters.BaseInFilter, dfilters.CharFilter):
    pass

class MyFilter(dfilters.FilterSet):
    author = dfilters.CharFilter()
    is_favorited = dfilters.BooleanFilter(method='get_is_favorited')
    tags = dfilters.AllValuesMultipleFilter(field_name = "tags__slug", lookup_expr="icontains")
    

    def get_is_favorited(self, queryset, name, value):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        user = get_object_or_404(User, username=self.request.user)
        favorite_recipes=Favorite.objects.filter(user=user).values('recipe')
        queryset = Recipe.objects.filter(pk__in=favorite_recipes)
        return queryset
    
    """def get_tags(self, queryset, name, values):
        print(values)
        print(self.request)
        print(self.request.url)
        return queryset.filter(tags__slug__in=values)"""

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)