from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/',  include('djoser.urls.authtoken')),
]