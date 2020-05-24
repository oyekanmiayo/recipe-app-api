from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


# Create your models here.
class UserManager(BaseUserManager):
    """Manager that provides functionality to create users and superusers."""

    def create_user(self, email, fname, lname, password=None, **extra_fields):
        """Create and save a new user."""
        if not email:
            raise ValueError("User must have an email")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            fname=fname,
            lname=lname,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, fname, lname, password):
        """Create and save a superuser."""
        user = self.create_user(email, fname, lname, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Model for all users in the system."""
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']


class Tag(models.Model):
    """Tag to be used for a recipe."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient to be used in a reciper"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
