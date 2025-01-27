from django.db import models
from django.core.validators import MinValueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=256)
    image = models.ImageField(
        'Изображение',
        upload_to='recipe_images',
        blank=True
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe'
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favourites(models.Model):
    user = models.ForeignKey(User, related_name='favourites_user', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='favourites_recipe', on_delete=models.CASCADE)


class ShopLsit(models.Model):
    user = models.ForeignKey(User, related_name='shop_user', on_delete=models.CASCADE)
    purchase = models.ForeignKey(Recipe, related_name='shop_purchase', on_delete=models.CASCADE)


class Subscriptions(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    subscription = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
