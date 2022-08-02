from django.db import models
from users.models import User


class Tag(models.Model):
    "Модель цветовых тэгов: завтрак, обед, ужин"
    name = models.CharField('Имя тэга', max_length=256, unique=True)
    slug = models.SlugField('Слаг тэга', max_length=256, unique=True)
    color =models.CharField('Цвет тэга', max_length=256, unique=True) 
    
    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    "Модель ингридиентов"
    name = models.CharField('Название', max_length=256, unique=True)
    measurement_unit =models.CharField('Единица измерения', max_length=50) 
    
    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    "Модель рецептов "
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='Ingredient_to_Recipe',
    )
    name = models.CharField('Название', max_length=256, unique=True)
    image = models.ImageField('Картинка', upload_to='recipe/')
    text = models.TextField('Описание')
    cooking_time = models.IntegerField('Время приготовления') 
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date',]


class Ingredient_to_Recipe(models.Model):
    "Модель связи ингридиентов и рецепта"
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ings'
    )
    amount = models.IntegerField('Количество') 
    
    def __str__(self):
        return f'{self.ingridients}-->{self.recipe}'