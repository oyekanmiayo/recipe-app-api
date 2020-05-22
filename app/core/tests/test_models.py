from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_is_successful(self):
        """Test creating a new user with an email is successful."""
        email = 'test@gmail.com'
        fname = 'test'
        lname = 'user'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            fname=fname,
            lname=lname,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_email_user_normalized(self):
        """Test new user's email is normalized."""
        email = 'test@GMAIL.COM'
        fname = 'test'
        lname = 'user'
        user = get_user_model().objects.create_user(
            email,
            fname,
            lname,
            'testpassword'
        )

        self.assertEqual(user.email, email.lower())

    def test_no_email_throws_value_error(self):
        """Test that a ValueError is thrown when email is None."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test', 'user')

    def test_super_user_with_email_is_successful(self):
        """Test creating a superuser is successful."""
        email = 'test@gmail.com'
        fname = 'test'
        lname = 'user'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            fname=fname,
            lname=lname,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
