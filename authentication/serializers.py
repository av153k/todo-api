from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from profiles.serializers import ProfileSerializer
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, max_length=128, min_length=8)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password', 'email', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=200, required=False)
    last_name = serializers.CharField(max_length=200, required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)

        if (username is None and email is None):
            raise serializers.ValidationError(
                'Email/Username is required to log in')

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')

        user = None
        if username is not None:
            user = authenticate(identifier=username, password=password)
        elif email is not None:
            user = authenticate(identifier=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'No user found for these credentials')

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.')

        return {
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': user.token,
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)
    profile = ProfileSerializer(write_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    profile_picture = serializers.CharField(
        source='profile.profile_picture', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password', 'email', 'profile', 'phone', 'profile_picture', 'token')
        read_only_fields = ['token']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for key, value in profile_data:
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance
