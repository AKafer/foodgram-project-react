
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from api.pagination import CustomPagination
from .serializers import  FollowSerializer, MyUserSerializer, MyUserSubsSerializer, MyUserCreateSerializer
from api.models import Follow
from api.mixin import MyCreateDestroyClass
from users.models import User

class UserViewSet(viewsets.ModelViewSet):
    "Класс представления юзеров"
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'create':
            return MyUserCreateSerializer
        return MyUserSerializer

    @action(methods=['get'], detail=False, url_path='me')
    def get_me(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = MyUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(methods=['post'], detail=False, url_path=r'(?P<id>\d+)/subscribe')
    def create_subsribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if user != author:
            Follow.objects.get_or_create(user=user, author=author)
            author_serializer = MyUserSubsSerializer(author)
            return Response(author_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK)
    

class SubscriptionViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pagination_class = CustomPagination
    serializer_class = MyUserSubsSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        authors = User.objects.filter(pk__in=subscribes)
        return authors  


class UserFollowViewSet(mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    "Класс удаление подписок"
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

    