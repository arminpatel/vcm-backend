from rest_framework import generics
from django.contrib.auth import get_user_model

from vcm_api.user.serializers import UserSerializer

User = get_user_model()


class RetrieveProfileView(generics.RetrieveAPIView):
    """ View to retrieve user """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
