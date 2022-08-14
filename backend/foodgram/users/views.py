
from api.models import Follow
from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from djoser.views import UserViewSet

from .serializers import (FollowSerializer, MyUserCreateSerializer,
                          MyUserSerializer, MyUserSubsSerializer)


class UserViewSet(viewsets.ModelViewSet):
    "Класс представления юзеров."
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
        """Функция предоставления данных о текущем пользователе."""
        user = get_object_or_404(User, username=request.user)
        serializer = MyUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        url_path='set_password',
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        user = get_object_or_404(User, username=request.user)
        if request.data['current_password'] == user.password:
            user.password = request.data['new_password']
            user.save()
            return HttpResponseRedirect(redirect_to='/api/recipes/')
        raise serializers.ValidationError(
            'Текущий пароль не верный')


class APIFollow(APIView):
    """Класс управления подписками."""
    def post(self, request, pk=None):
        user = get_object_or_404(User, username=request.user)
        author = get_object_or_404(User, pk=pk)
        serializer = FollowSerializer(data={"user": user.pk, "author": pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author_serializer = MyUserSubsSerializer(author)
        return Response(
            author_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk=None):
        user = get_object_or_404(User, username=request.user)
        follow = get_object_or_404(Follow, user=user, author=pk)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """Класс представления списка подписок текущего пользователя."""
    pagination_class = CustomPagination
    serializer_class = MyUserSubsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        return User.objects.filter(pk__in=subscribes)
