from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, TokenClass
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]