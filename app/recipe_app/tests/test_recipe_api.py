from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe_app.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe_app:recipe-list')


def detail_url(recipe_id):
    """Return recipe detail url."""
    return reverse('recipe_app:recipe-detail', args=[recipe_id])


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': 5.00
    }

    # defaults.update updates the default dictionary's
    # default values
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


def create_sample_tag(user, name='savoury'):
    """Create and return sample tag"""
    return Tag.objects.create(user=user, name=name)


def create_sample_ingredients(user, name='mushrooms'):
    """Create and return sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


class PublicRecipeAPITests(TestCase):
    """Test endpoints that don't require authentication."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_to_view_ingredients(self):
        """Test that authentication is needed to view the ingredients."""

        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesAPITests(TestCase):
    """Test endpoints that require authentication."""

    def setUp(self):
        self.client = APIClient()

        self.user = create_user(
            fname='Test',
            lname='User',
            email='test@gmail.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes_is_successful(self):
        """Test retrieving a list of recipes is successful"""

        create_sample_recipe(user=self.user)
        payload = {'title': 'Carrot'}
        create_sample_recipe(user=self.user, **payload)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieved_recipes_is_for_user(self):
        """Test that only the user's recipes are retrieved."""

        user2 = create_user(
            fname='Test2',
            lname='User2',
            email='test2@gmail.com',
            password='test2pass'
        )

        # Check test_retrieved_ingredients_limited_to_user
        # It's a diff approach to solving the same problem
        create_sample_recipe(user=user2)
        payload = {'title': 'Carrot'}
        create_sample_recipe(user=self.user, **payload)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_viewing_recipe_detail_is_successful(self):
        """Test viewing a recipe's detail is successful."""

        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        recipe.ingredients.add(create_sample_ingredients(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating recipe."""

        payload = {
            'title': 'Chocolate Cake',
            'time_minutes': 5,
            'price': 10.00
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))
            # getattr(recipe, key) = recipe[key] == recipe.key ?

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags."""

        tag1 = create_sample_tag(user=self.user, name='Tag 1')
        tag2 = create_sample_tag(user=self.user, name='Tag 2')

        payload = {
            'title': 'Chocolate Cake2',
            'time_minutes': 5,
            'price': 10.00,
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients."""

        ingredient1 = create_sample_ingredients(user=self.user, name='Ing 1')
        ingredient2 = create_sample_ingredients(user=self.user, name='Ing 2')

        payload = {
            'title': 'Chocolate Cake3',
            'time_minutes': 5,
            'price': 10.00,
            'ingredients': [ingredient1.id, ingredient2.id]
        }

        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_partial_update_recipe(self):
        """Test partially updating the recipe."""
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))

        new_tag = create_sample_tag(user=self.user, name='Tag 2')

        payload = {'title': 'Recipe Update', 'tags': [new_tag.id]}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_recipe(self):
        """Test fully updating the recipe."""
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))

        payload = {
            'title': 'Oha Soup',
            'time_minutes': 12,
            'price': 15.00
        }

        url = detail_url(recipe.id)
        self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        # Why is res.data['price'] == 15.0 instead of 15.00?
        self.assertEqual(recipe.price, payload['price'])

        tags = recipe.tags.all()
        self.assertEqual(len(tags), 0)
