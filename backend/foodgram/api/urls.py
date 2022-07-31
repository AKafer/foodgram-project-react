from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, TokenClass

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'auth', TokenClass, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]