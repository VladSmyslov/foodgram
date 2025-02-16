from django.contrib import admin

from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    IngredientsRecipe,
    Favourites,
    ShopLsit,
    Subscriptions
)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')
    list_filter = ('tags',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientsRecipe)
admin.site.register(Favourites)
admin.site.register(ShopLsit)
admin.site.register(Subscriptions)
