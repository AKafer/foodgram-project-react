# Generated by Django 3.2.15 on 2022-08-09 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220809_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название'),
        ),
    ]