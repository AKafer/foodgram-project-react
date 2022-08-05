from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserFollowViewSet, FollowPostDelete


router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'users/subscriptions', UserFollowViewSet, basename='user_subs')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'users/(?P<id>\d+)/subscribe', FollowPostDelete, basename='subscribes')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/',  include('djoser.urls.authtoken')),
]