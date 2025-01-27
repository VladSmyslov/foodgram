from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())
    is_favorited = filters.BooleanFilter(method='is_favorited_method')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_method'
    )

    def is_favorited_method(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favourites_recipe__user=user)
        return queryset

    def is_in_shopping_cart_method(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shop_purchase__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
