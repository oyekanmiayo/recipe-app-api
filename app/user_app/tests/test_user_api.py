from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user_app:create')
AUTHENTICATE_URL = reverse('user_app:authenticate')
MANAGE_URL = reverse('user_app:manage')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class CreatUserAPITests(TestCase):
    """Test creating users via the API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_is_successfully(self):
        """Test creating user with valid payload is successful."""
        payload = {
            'email': 'test@gmail.com',
            'fname': 'Test',
            'lname': 'User',
            'password': 'password'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_duplicate_user_fails(self):
        """Test creating user that already exists fails."""
        payload = {
            'email': 'ayomideoyekanmi@gmail.com',
            'fname': 'Test',
            'lname': 'User',
            'password': 'password'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_that_password_too_short_returns_400(self):
        """Test that the password must be > 5 characters"""
        payload = {
            'email': 'ayomideoyekanmi@gmail.com',
            'fname': 'Test',
            'lname': 'User',
            'password': 'ps'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)


class AuthenticateUserAPITests(TestCase):
    """Test authenticating users via an API."""

    def setUp(self):
        self.client = APIClient()

    def test_token_is_created_for_valid_user(self):
        """Test that token is created for valid user."""

        payload = {
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@gmail.com',
            'password': 'testPass'
        }

        create_user(**payload)
        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_not_created_for_invalid_credentials(self):
        """Test that token is not created for invalid credentials."""
        create_payload = {
            'fname': 'Test',
            'lname': 'User',
            'email': 'test@gmail.com',
            'password': 'testPass'
        }

        create_user(**create_payload)

        req_payload = {
            'email': 'test@gmail.com',
            'password': 'testgmail'
        }
        res = self.client.post(AUTHENTICATE_URL, req_payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_for_nonexistent_user(self):
        """Test that token is not created if user doesn't exist."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'testPass'
        }
        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_not_created_for_missing_key_fields(self):
        """Test that token is not created when key fields are missing."""

        payload = {
            'email': 'test@gmail.com',
            'password': ''
        }
        res = self.client.post(AUTHENTICATE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ManageUserWithoutTokenAPITests(TestCase):
    """Test managing - view, update, delete -  via APIs without auth"""

    def test_retrieve_user_without_token_unauthorized(self):
        """Test that users cannot be viewed without a token."""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class ManageUserWithTokenAPITests(TestCase):
    """Test managing - view, update, delete -  via APIs. Requires auth"""

    def setUp(self):
        self.user = create_user(
            fname='Test',
            lname='User',
            email='test@gmail.com',
            password='testpass'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_with_token_successful(self):
        """Test that users can be viewed when authenticated."""
        res = self.client.get(MANAGE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'fname': self.user.fname,
            'lname': self.user.lname,
            'email': self.user.email
        })

    def test_post_method_not_allowed_on_manage_url(self):
        """Test that post is not allowed on manage url."""
        res = self.client.post(MANAGE_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_with_token_successful(self):
        """
        Test updating user's profile is successful with authenticated user
        """
        payload = {
            'fname': 'Testing',
            'lname': 'Userer',
            'password': 'panda'
        }

        res = self.client.patch(MANAGE_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.fname, payload['fname'])
        self.assertEqual(self.user.lname, payload['lname'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
