
from rest_framework import mixins, viewsets


class CustomGetRetrieveClass(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    "Кастомный миксин класс для тэгов и ингредиентов"
    pass
