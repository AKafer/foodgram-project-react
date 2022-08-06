from django.contrib import admin

from .models import Follow, Tag, Tag_to_Recipe, Ingredient, Recipe, Favorite

class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'cooking_time', 'image', 'pub_date'
    )
    empty_value_display = '-пусто-'


admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Tag)
admin.site.register(Tag_to_Recipe)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
