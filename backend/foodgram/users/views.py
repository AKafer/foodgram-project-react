from rest_framework import  status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, TokenGeneratorSerialiser, UserMeSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserViewSet(viewsets.ModelViewSet):
    """Класс представления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def mi_signin(self, request):
        username =request.user
        me = get_object_or_404(User, username=username)
        serializer = UserMeSerializer(me)
        return Response(serializer.data, status=status.HTTP_200_OK)

        """
        return Response({
            "email": me.email,
            "id": me.id,
            "username": me.username,
            "first_name": me.first_name,
            "last_name": me.last_name,
            "is_subscribed": False
        })
        """

class TokenClass(viewsets.ModelViewSet):
    """Класс авторизации пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
  
    @action(detail=False, methods=['post'], url_path='token/login')
    def tokengenerator(self, request):
        """Функция генерациии токена по юзернейму и коду."""
        serializer = TokenGeneratorSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        password = request.data['password']
        user = get_object_or_404(User, email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'auth_token': str(refresh.access_token)})
    

