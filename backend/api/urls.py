from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, MyUserViewSet, RecipesViewSet,
                       TagsViewSet)

router = DefaultRouter()
router.register('users', MyUserViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
