from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import APIFollow, SubscriptionViewSet

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(
    r'users/subscriptions',
    SubscriptionViewSet,
    basename='subscriptions'
)
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('users/<pk>/subscribe/', APIFollow.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
