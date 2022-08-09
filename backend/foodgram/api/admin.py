from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, Tag_to_Recipe)


class TagInline(admin.TabularInline):
    model = Tag_to_Recipe
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'image', 'pub_date'
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'author__username')
    list_filter = ('tags', 'pub_date',)
    inlines = (TagInline,)
    readonly_fields = ('count_add_favorited',)
    empty_value_display = '-пусто-'

    def count_add_favorited(self, obj):
        count = Favorite.objects.filter(recipe=obj).count()
        return count
    
    count_add_favorited.short_description = 'Сколько раз добавлен в избранное'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ()

class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'recipe', 'measurement_unit', 'amount')
    list_display_links = ('id', 'name')
    readonly_fields = ('name',)
    empty_value_display = '-пусто-'

class TagtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_display_links = ('id', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Tag, TagtAdmin)
admin.site.register(Tag_to_Recipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)

