from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeViewSet, TagViewSet, FavoritePostDelete
from users.views import  UserViewSet, UserFollowViewSet


router = DefaultRouter()

router.register(r'users/(?P<id>\d+)/subscribe', UserFollowViewSet, basename='subscribes')
router.register(r'users', UserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes/(?P<id>\d+)/favorite', FavoritePostDelete, basename='favorite')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/',  include('djoser.urls.authtoken')),
]