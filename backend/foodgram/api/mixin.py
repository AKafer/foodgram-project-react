
from rest_framework import mixins, viewsets


class MyCreateDestroyClass(mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    "Кастомный миксин класс"
    pass