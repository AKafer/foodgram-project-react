from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag, TagRecipe)


class TagInline(admin.TabularInline):
    """Вспомогательный класс для отображения тэгов в модели рецептов"""
    model = TagRecipe
    extra = 3


class IngredientsInline(admin.TabularInline):
    """Вспомогательный класс для отображения игредиентов в модели рецептов"""
    model = IngredientAmount
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    """Класс отображения в админке модели рецептов"""
    inlines = (TagInline, IngredientsInline)
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'image', 'pub_date'
    )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'author__username')
    list_filter = ('tags', 'pub_date',)
    readonly_fields = ('count_add_favorited',)
    empty_value_display = '-пусто-'

    def count_add_favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    count_add_favorited.short_description = 'Сколько раз добавлен в избранное'


class IngredientAdmin(admin.ModelAdmin):
    """Класс отображения в админке модели ингедиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    list_editable = ()


class IngredientAmountAdmin(admin.ModelAdmin):
    """Класс отображения в админке модели ингредиентов в рецептах"""
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    list_display_links = ('id', 'ingredient')
    empty_value_display = '-пусто-'


class TagtAdmin(admin.ModelAdmin):
    """Класс отображения в админке модели тэгов"""
    list_display = ('id', 'name', 'slug', 'color')
    list_display_links = ('id', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Tag, TagtAdmin)
admin.site.register(TagRecipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
