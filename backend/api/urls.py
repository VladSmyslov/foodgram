from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (
    RecipesViewSet,
    TagsViewSet,
    IngredientViewSet,
    MyUserViewSet)

router = DefaultRouter()
router.register('users', MyUserViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # path('users/me/avatar/', AvatarUpdateView.as_view()),
    # path('users/', include(router.urls)),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
