from recipes.models import (Favourites, Ingredient,
                            IngredientsRecipe, Recipe,
                            ShopLsit, Subscriptions, Tag)
from django.contrib import admin


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'in_favourites')
    search_fields = ('name', 'author__email')
    list_filter = ('tags',)
    readonly_fields = ('in_favourites',)

    @admin.display(description='В избранном')
    def in_favourites(self, obj):
        return obj.favourites_recipe.count()


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
