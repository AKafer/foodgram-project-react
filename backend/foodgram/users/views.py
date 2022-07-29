from rest_framework import  viewsets
from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    """Класс представления пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = ('username')

