from rest_framework import generics
from django.contrib.auth import get_user_model

from vcm_api.user.serializers import UserSerializer
from vcm_api.user.permissions import IsOwnerOrAdminOrReadOnly

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """ View to create a new user """
    model = User
    serializer_class = UserSerializer


class RetrieveUpdateProfileView(generics.RetrieveUpdateAPIView):
    """ View to retrieve and update user """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
