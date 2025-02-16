import short_url
from django.http import HttpResponse
from django.db.models import Exists, Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from djoser.views import UserViewSet
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from .permissions import IsAuthorOrReadOnly
# from api.permissions import PostPermission
from .filters import RecipeFilter
from recipes.models import (
    Recipe,
    Ingredient,
    IngredientsRecipe,
    Tag,
    User,
    Favourites,
    ShopLsit,
    Subscriptions
)
from api.serializers import (
    Base64ImageField,
    RecipeListSerializer,
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeToFavoriteSerializer,
    MyUserSerializer,
    CreateSubscribeSerializer,
    AvatarSerializer
)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeListSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('tags__slug', 'author')
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            fav_recipe, created = Favourites.objects.get_or_create(
                user=user,
                recipe=recipe
            )
            if not created:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeToFavoriteSerializer(fav_recipe.recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            del_recipe = Favourites.objects.filter(
                user=user,
                recipe=recipe
            ).first()
            if not del_recipe:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            del_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            purchase, created = ShopLsit.objects.get_or_create(
                user=user,
                purchase=recipe
            )
            if not created:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = RecipeToFavoriteSerializer(purchase.purchase)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            del_purchase = ShopLsit.objects.filter(
                user=user,
                purchase=recipe
            )
            if not del_purchase.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            del_purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def _create_shopping_txt(self, ingredients):
        shopping_list = [
            (f"{ingredient['name__name']}: "
             f"{ingredient['total_amount']} "
             f"{ingredient['name__measurement_unit']}\n")
            for ingredient in ingredients
        ]
        return '\n'.join(shopping_list) + '\n'

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = IngredientsRecipe.objects.filter(
            recipe__shop_purchase__user=user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'

        ).annotate(total=Sum('amount'))
        shopping_list = self._create_shopping_txt(ingredients)
        return HttpResponse(shopping_list, content_type='text/plain')
        # return Response(status=status.HTTP_200_OK)

    @action(
        methods=['get'],
        detail=True,
        url_path='get-link',
        permission_classes=(AllowAny,)
    )
    def get_link(self, request, pk=None):
        get_object_or_404(Recipe, id=pk)
        link = request.build_absolute_uri(f'/r/{pk}/')
        return Response(
            {'short-link': link},
            status=status.HTTP_200_OK
        )


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    http_method_names = ['get', ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AllowAny, ]
    http_method_names = ['get', ]


class MyUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_update(self, serializer):
        serializer.save(avatar=self.request.data['avatar'])

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscription__owner=self.request.user
        )
        recipes_limit = request.query_params.get('recipes_limit')
        if subscriptions:
            pages = self.paginate_queryset(subscriptions)
            serializer = CreateSubscribeSerializer(
                pages,
                many=True,
                context={'request': request, 'recipes_limit': recipes_limit}
            )
            return self.get_paginated_response(serializer.data)
        return Response('Вы ни на кого не подписаны.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        subscription_object = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            subscription, created = Subscriptions.objects.get_or_create(
                owner=user,
                subscription=subscription_object
            )
            if not created or subscription_object == user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            # subscription.save()
            recipes_limit = request.query_params.get('recipes_limit')
            serializer = CreateSubscribeSerializer(
                subscription_object,
                context={'request': request, 'recipes_limit': recipes_limit}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            del_subscription = Subscriptions.objects.filter(
                owner=user,
                subscription=subscription_object
            )
            if not del_subscription.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            del_subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['put', 'delete'],
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,),
        serializer_class=AvatarSerializer
    )
    def avatar(self, request):
        user = request.user
        serializer = MyUserSerializer(user, data=request.data, partial=True)

        if request.method == 'DELETE':
            if user.avatar:
                user.avatar.delete(save=True)
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"avatar": user.avatar.url},
                        status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = MyUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AvatarUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AvatarSerializer
