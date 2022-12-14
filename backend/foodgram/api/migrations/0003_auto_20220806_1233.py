# Generated by Django 2.2.16 on 2022-08-06 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220805_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=50, verbose_name='Единица измерения')),
                ('amount', models.IntegerField(verbose_name='Количество')),
            ],
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.DeleteModel(
            name='Ingredient_to_Recipe',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.IngredientAmount'),
            preserve_default=False,
        ),
    ]
