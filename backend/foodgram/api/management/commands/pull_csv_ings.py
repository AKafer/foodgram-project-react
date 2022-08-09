import pandas as pd
import json
import os

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    print(os.path.abspath(os.curdir))
    Ingredient.objects.all().delete()
    def handle(self, *args, **options):
        with open('C:\\Dev\\foodgram-project-react\\data\\ingredients.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for d in data:
            Ingredient.objects.get_or_create(name=str(d['name']), measurement_unit=str(d['measurement_unit'])) 
        print('Данные записаны в БД')

 
        
        
        
        """tmp_data = pd.read_csv('C:\\Dev\\foodgram-project-react\\data\\ingredients.csv', sep=',')
        ings = [
            Ingredient(
                name=tmp_data.iloc[:, [0]],
                measurement_unit=tmp_data.iloc[:, [1]],
            )
            for i, row in tmp_data.iterrows()
        ]
        Ingredient.objects.bulk_create(ings)
        print('Данные записаны в БД')"""