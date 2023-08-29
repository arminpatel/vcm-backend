from rest_framework.generics import CreateAPIView, ListAPIView
from vcm_api.submission.serializers import SubmissionSerializer, SubmissionListSerializer
from rest_framework.permissions import IsAuthenticated
from vcm_api.submission.permissions import IsContestCreatorOrParticipantOrAdmin
from rest_framework.exceptions import NotFound
from vcm_api.submission.models import Submission
from vcm_api.contest.models import Contest
from vcm_api.problem.models import Problem
from django.contrib.auth import get_user_model


class CreateSubmissionView(CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, IsContestCreatorOrParticipantOrAdmin, )


class ListContestSubmission(ListAPIView):
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        contest_id = self.kwargs['contestid']
        query_contest = Contest.objects.filter(id=contest_id).first()

        if query_contest is None:
            raise NotFound()

        query_problems = Problem.objects.filter(contest=query_contest).values_list('id', flat=True)
        queryset = Submission.objects.filter(problem__in=query_problems)
        return queryset


class ListUserContestSubmission(ListAPIView):
    serializer_class = SubmissionListSerializer

    def get_queryset(self):
        User = get_user_model()
        contest_id = self.kwargs['contestid']
        query_username = self.kwargs['username']
        query_contest = Contest.objects.filter(id=contest_id).first()
        query_user = User.objects.filter(username=query_username).first()

        if query_contest is None or query_user is None:
            raise NotFound()

        query_problems = Problem.objects.filter(contest=query_contest).values_list('id', flat=True)
        queryset = Submission.objects.filter(problem__in=query_problems, user=query_user)
        return queryset
