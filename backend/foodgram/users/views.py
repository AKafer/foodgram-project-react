
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from api.pagination import CustomPagination
from .serializers import  FollowSerializer, MyUserSerializer, MyUserSubsSerializer
from api.models import Follow
from api.mixin import MyCreateDestroyClass
from users.models import User


class UserFollowViewSet(viewsets.ModelViewSet):
    "Класс представления подписок юзера"
    serializer_class = MyUserSubsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        return User.objects.filter(pk__in=subscribes)

class FollowPostDelete(MyCreateDestroyClass):
    "Класс представления рецептов"
    serializer_class = MyUserSubsSerializer

    """ def get_queryset(self):
        print('ППППППППППППППППППППППППППППППППППППППППППППППППППППППППП')
        user = get_object_or_404(User, username=self.request.user)
        author_id = self.kwargs.get('id')
        print(author_id)
        author = get_object_or_404(User, pk=author_id)
        print(author)
        if user != author:
            Follow.objects.create(user=user, author=author)
            return author
        return author
            
        return Response(author_serializer.data, status=status.HTTP_200_OK)"""

    #def perform_create(self, serializer):
    @action(methods=['post'], detail=False)
    def new_create(self, request, **kwargs):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        user = self.request.user
        print(user)
        author_id = self.kwargs.get('id')
        print(author_id)
        author = get_object_or_404(User, pk=author_id)
        print(author)
        if user != author:
            Follow.objects.create(user=user, author=author)
            author_serializer = MyUserSubsSerializer(author)
            return Response(author_serializer.data, status=status.HTTP_201_CREATED)
        return Response(author_serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        follow = Follow.objects.filter(user=user, author=author).first()
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    