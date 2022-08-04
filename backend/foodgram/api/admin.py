from django.contrib import admin

from .models import Tag, Tag_to_Recipe, Ingredient, Ingredient_to_Recipe, Recipe


admin.site.register(Tag)
admin.site.register(Tag_to_Recipe)
admin.site.register(Ingredient)
admin.site.register(Ingredient_to_Recipe)
admin.site.register(Recipe)
