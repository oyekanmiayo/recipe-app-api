from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe_app.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe_app:recipe-list')


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
