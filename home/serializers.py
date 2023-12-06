from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.utils.crypto import get_random_string
import hashlib

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio']
        # read_only_fields = ['user', 'id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError('Name is required')
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Email is required')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username is already taken')
        return value

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        email = validated_data.get('email')

        email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()

        username = f"{first_name.lower()}_{email_hash}"

        user = User.objects.create_user(username=username, **validated_data)
        return user
