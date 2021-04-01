from .models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    phone = serializers.CharField(max_length=11, required=False)
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone', 'profile_picture']
        read_only_fields = ['username']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
