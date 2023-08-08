from rest_framework.generics import CreateAPIView
from vcm_api.submission.serializers import SubmissionSerializer
from rest_framework.permissions import IsAuthenticated
from vcm_api.submission.permissions import IsContestCreatorOrParticipantOrAdmin


class CreateSubmissionView(CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, IsContestCreatorOrParticipantOrAdmin, )
