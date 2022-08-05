
from rest_framework import mixins, viewsets


class MyCreateDestroyClass(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    "Кастомный миксин класс"
    pass