from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = get_user_model()
        fields = ('fname', 'lname', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """Create and return a new user."""
        user = get_user_model().objects.create_user(
            **validated_data
        )

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object."""
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )

            if not user:
                msg = _("Unable to authenticate with provided credentials")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _("Must include email and password to authenticate")
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
