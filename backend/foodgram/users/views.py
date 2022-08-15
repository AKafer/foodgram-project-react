
from api.models import Follow
from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .serializers import FollowSerializer, MyUserSubsSerializer


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
