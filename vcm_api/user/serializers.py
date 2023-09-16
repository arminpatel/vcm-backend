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

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['profile'] = data.get('profile', {})
        return ret

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if not profile_data:
            profile_data = {}
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile = instance.profile
            profile.cf_handle = profile_data.get('cf_handle',
                                                 profile.cf_handle)
            profile.cc_handle = profile_data.get('cc_handle',
                                                 profile.cc_handle)
            profile.ac_handle = profile_data.get('ac_handle',
                                                 profile.ac_handle)
            profile.save()
        validated_data.pop('password', None)
        validated_data.pop('username', None)
        return super().update(instance, validated_data)
