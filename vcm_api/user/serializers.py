from rest_framework import serializers
from vcm_api.user.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['cf_handle', 'cc_handle', 'ac_handle']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user
