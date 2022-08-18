from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель цветовых тэгов: завтрак, обед, ужин"""
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Наименование')
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг')
    color = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Цвет в формате #XXXXXX'
    )

    def __str__(self):
        return f'{self.slug}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    """Модель ингридиентов"""
    name = models.CharField(max_length=256, verbose_name='Наименование')
    measurement_unit = models.CharField(
        max_length=50, verbose_name='Ед. измерения')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='res_ings',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='tag_recipe',
        verbose_name='Тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='Ingredient_recipe',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(max_length=256, verbose_name='Название')
    image = models.ImageField(upload_to='recipe/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Порядок приготовления')
    cooking_time = models.PositiveIntegerField(verbose_name='Время готовки')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date', ]


class IngredientAmount(models.Model):
    """Кастомная модель свяизи ингридиентов и рецептов"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Инредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.amount}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class TagRecipe(models.Model):
    """Кастомная модель связи тэгов и рецепта"""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Наименование'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags_ref',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.recipe}<-->{self.tag}'

    class Meta:
        verbose_name = 'Тэг в рецепте'
        verbose_name_plural = 'Тэги в рецепте'


class Follow(models.Model):
    """Модель подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    def __str__(self):
        return f'{self.user}-->{self.author}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'


class Favorite(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.user}-->{self.recipe}'

    class Meta:
        verbose_name = 'Избравнный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCart(models.Model):
    """Модель списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.user}-->{self.recipe}'

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'
