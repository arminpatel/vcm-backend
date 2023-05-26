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
        fields = ['username', 'first_name', 'last_name', 'profile']
