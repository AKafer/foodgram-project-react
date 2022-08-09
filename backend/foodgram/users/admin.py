from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'password'
    )
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
