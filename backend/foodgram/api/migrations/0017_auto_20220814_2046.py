# Generated by Django 2.2.16 on 2022-08-14 17:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20220812_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagrecipe',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='api.Tag', verbose_name='Наименование'),
        ),
    ]
