from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient
from recipe_app import serializers


class BaseViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """
    This class was created because TagViewSet and IngredientViewSet
    had a lot of common code, so it just makes sense to have it all
    in one place so that it can be extended.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object."""
        return serializer.save(user=self.request.user)


class TagViewSet(BaseViewSet):
    """Manage Tags in the database."""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseViewSet):
    """Manage Ingredients in the database."""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
