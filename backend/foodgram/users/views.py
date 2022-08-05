
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from api.pagination import CustomPagination
from .serializers import  FollowSerializer, MyUserSerializer
from api.models import Follow
from users.models import User


class UserFollowViewSet(viewsets.ModelViewSet):
    "Класс представления подписок юзера"
    serializer_class = MyUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        subscribes = Follow.objects.filter(user=user).values('author')
        return User.objects.filter(pk__in=subscribes)

class FollowPostDelete(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    "Класс представления рецептов"
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        user = self.request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        if not Follow.objects.filter(user=user, author=author).exists() and user != author:
            serializer.save(user=self.request.user, author=author)
    
    @action(methods=['delete'], detail=False)
    def delete(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, pk=author_id)
        follow = Follow.objects.filter(user=user, author=author).first()
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


