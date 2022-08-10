
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.models import Follow
from api.pagination import CustomPagination
from users.models import User

from .serializers import (MyUserCreateSerializer, MyUserSerializer,
                          MyUserSubsSerializer)


class UserViewSet(viewsets.ModelViewSet):
    "Класс представления юзеров"
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return MyUserCreateSerializer
        return MyUserSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_me(self, request):
        """Функция предоставления данных о текущем пользователе"""
        user = get_object_or_404(User, username=request.user)
        serializer = MyUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=False,
        url_path=r'(?P<id>\d+)/subscribe'
    )
    def subsribe_add_del(self, request, id=None):
        """Функция добавления/удаления подписки"""
        user = request.user
        author = get_object_or_404(User, pk=id)
        if str(self.request.method) == 'POST':
            if user != author:
                Follow.objects.get_or_create(user=user, author=author)
                author_serializer = MyUserSubsSerializer(author)
                return Response(
                    author_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_200_OK)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Класс представления списка подписок текущего пользователя"""
    pagination_class = CustomPagination
    serializer_class = MyUserSubsSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        return User.objects.filter(pk__in=subscribes)
