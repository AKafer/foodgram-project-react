from django.db import models


class Tag(models.Model):
    name = models.CharField('Имя тэга', max_length=256, unique=True)
    slug = models.SlugField('Слаг тэга', max_length=256, unique=True)
    color =models.CharField('Цвет тэга', max_length=256, unique=True) 
    
    def __str__(self):
        return self.slug