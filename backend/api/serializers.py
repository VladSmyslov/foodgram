import base64

from django.core.files.base import ContentFile

from djoser.serializers import UserCreateSerializer

from rest_framework import serializers

from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe, Tag, Ingredient, IngredientsRecipe, User, Favourites, ShopLsit, Subscriptions


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsRecipeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', required=False)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        required=False
    )

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientsInRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для добавления ингредиента в рецепт.'''
    id = serializers.IntegerField(required=True)

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeToFavoriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    image = Base64ImageField(required=False, allow_null=True)
    cooking_time = serializers.IntegerField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')

    def create(self, validated_data):
        recipe_id = self.context['kwargs'].get('recipes_id')
        favourites = self.context['request'].user
        recipe = Recipe.objects.get(recipe_id)
        self.favourites.set(favourites)
        return recipe


class RecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания рецепта.'''
    ingredients = AddIngredientsInRecipeSerializer(many=True)
    image = Base64ImageField(allow_null=True)
    # tags = AddTagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=True
    )

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        ingredients_uniq = []
        for ingredient in ingredients:
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError()
            if ingredient in ingredients_uniq:
                raise serializers.ValidationError()
            ingredients_uniq.append(ingredient)
        if len(value) < 1:
            raise serializers.ValidationError()
        return value

    def validate_tags(self, value):
        tags = self.initial_data.get('tags')
        tags_unniq = []
        for tag in tags:
            if tag in tags_unniq:
                raise serializers.ValidationError()
            tags_unniq.append(tag)
        if len(tags) < 1:
            raise serializers.ValidationError()
        return value

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientsRecipe.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        if not validated_data.get('tags') or not validated_data.get('ingredients'):
            raise serializers.ValidationError()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientsRecipe.objects.create(
                ingredient=current_ingredient, recipe=instance, amount=amount)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeListSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data


class MyUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

    def get_is_subscribed(self, obj):
        return (
            Subscriptions.objects.filter(
                owner=obj.id,
                subscription=obj
            ).exists()
        )


class CreateSubscribeSerializer(serializers.ModelSerializer):
    # recipes = RecipeToFavoriteSerializer(read_only=True, many=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar'
        )

    def get_recipes_count(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return len(recipes)



    """ def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        User.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            current_ingredient = Ingredient.objects.get(pk=ingredient_id)
            IngredientsRecipe.objects.create(
                ingredient=current_ingredient, recipe=instance, amount=amount)
        instance.save()
        return instance """

    def get_is_subscribed(self, obj):
        return (True)

    def get_recipes(self, obj):
        # request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = RecipeToFavoriteSerializer(recipes, many=True)
        return serializer.data


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = IngredientsRecipeListSerializer(
        source='ingredient_list',
        many=True
    )
    tags = TagSerializer(many=True)
    author = MyUserSerializer(read_only=True, )
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Favourites.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and ShopLsit.objects.filter(
                user=self.context['request'].user,
                purchase=obj
            ).exists()
        )


class AvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)
