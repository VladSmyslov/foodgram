from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()

MIN_VALUE = 1
MAX_VALUE = 32000


class Tag(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг',)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=256)
    measurement_unit = models.CharField('Единица измерения', max_length=10)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField('Название', max_length=256)
    image = models.ImageField(
        'Изображение',
        upload_to='recipe_images',
        blank=True
    )
    text = models.TextField('Текстовое описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тег')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE)]
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ingredient_list'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецептах'
        verbose_name_plural = 'Ингредиент в рецепте'
        ordering = ['ingredient']

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favourites(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favourites_user',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='favourites_recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['user']

    def __str__(self):
        return self.recipe.name


class ShopLsit(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shop_user',
        on_delete=models.CASCADE
    )
    purchase = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='shop_purchase',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'покупки'
        verbose_name_plural = 'Покупки'
        ordering = ['user']

    def __str__(self):
        return self.purchase.name


class Subscriptions(models.Model):
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец подписки',
        on_delete=models.CASCADE,
        related_name='owner'
    )
    subscription = models.ForeignKey(
        User,
        verbose_name='Подписка',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    class Meta:
        verbose_name = 'подписки'
        verbose_name_plural = 'Подписки'
        ordering = ['owner']

    def __str__(self):
        return self.owner.first_name
