from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView
from vcm_api.contest.models import Contest
from django.contrib.auth import get_user_model
from vcm_api.contest.serializers import ContestSerializer
from vcm_api.contest.permissions import IsContestCreatorOrAdminOrReadOnly
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class RetrieveUpdateContestView(RetrieveUpdateAPIView):
    """View to retrieve specific contest"""
    permission_classes = (IsAuthenticatedOrReadOnly, IsContestCreatorOrAdminOrReadOnly,)
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer


class ListParticipantContestView(ListAPIView):
    """View to List all the contest"""

    def get_queryset(self):
        sentusername = self.kwargs['username']
        User = get_user_model()
        query_user = User.objects.filter(username=sentusername).first()

        if (query_user is None):
            raise NotFound(detail='User does not exist')

        queryset = query_user.participated_in
        return queryset

    serializer_class = ContestSerializer


class CreateContestView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Contest
    serializer_class = ContestSerializer
