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
        through='Tag_to_Recipe',
        related_name='tag_recipe',
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


class IngredientAmount(models.Model):
    "Модель ингридиентов"
    name = models.CharField('Название', max_length=256)
    measurement_unit =models.CharField('Единица измерения', max_length=50)
    amount = models.IntegerField('Количество')
    recipe =  models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name = 'ingredients'
    )
    
    def __str__(self):
        return f'{self.name}'


class Tag_to_Recipe(models.Model):
    "Модель связи тэгов и рецепта"
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_ref'
    )
    
    def __str__(self):
        return f'{self.tag}-->{self.recipe}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    def __str__(self):
        return f'{self.user}-->{self.author}'

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}-->{self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user}-->{self.recipe}'