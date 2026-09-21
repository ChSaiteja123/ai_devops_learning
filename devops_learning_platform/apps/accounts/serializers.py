"""
Accounts Serializers.

WHAT IS A DRF SERIALIZER?
--------------------------
A serializer converts complex Python objects (model instances, querysets)
into simple data types (dicts, lists) that can be rendered into JSON.

It also does the reverse: validates incoming JSON and converts it back
into Python objects for saving to the database.

Think of it as a two-way translator:
  Python Model ↔ Serializer ↔ JSON
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Public user info — safe to expose to other users.
    No private fields like email.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'skill_level', 'bio', 'github_username']
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    """
    Full user profile — for the authenticated user's own profile.
    """
    full_name = serializers.ReadOnlyField()
    total_points = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'bio', 'avatar', 'skill_level', 'github_username',
            'linkedin_url', 'website_url', 'location', 'years_of_experience',
            'is_premium', 'total_points', 'date_joined', 'created_at',
        ]
        read_only_fields = ['id', 'date_joined', 'created_at', 'is_premium', 'total_points']


class RegisterSerializer(serializers.ModelSerializer):
    """
    User registration serializer.

    Validates that:
    - Username is unique
    - Email is unique
    - Password meets Django's validators
    - Password confirmation matches
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'skill_level']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password!
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Change password for authenticated users."""
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Current password is incorrect.')
        return value
