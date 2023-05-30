from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from vcm_api.contest.models import Contest
from django.contrib.auth import get_user_model
from vcm_api.contest.serializers import RetrieveContestSerializer
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated


class RetrieveContestView(RetrieveAPIView):
    """View to retrieve specific contest"""
    queryset = Contest.objects.all()
    serializer_class = RetrieveContestSerializer


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

    serializer_class = RetrieveContestSerializer

class CreateContestView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    model = Contest
    serializer_class = RetrieveContestSerializer