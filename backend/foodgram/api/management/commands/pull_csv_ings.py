import json
import os

from api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    print(os.path.abspath(os.curdir))
    Ingredient.objects.all().delete()

    def handle(self, *args, **options):
        with open(
            'C:\\Dev\\foodgram-project-react\\data\\ingredients.json',
            'r',
            encoding='utf-8'
        ) as f:
            data = json.load(f)
        for d in data:
            Ingredient.objects.get_or_create(
                name=str(d['name']),
                measurement_unit=str(d['measurement_unit'])
            )
        print('Данные записаны в БД')
