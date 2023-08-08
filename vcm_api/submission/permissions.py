from rest_framework import permissions
from vcm_api.problem.models import Problem


class IsContestCreatorOrParticipantOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if "problem_id" not in request.data:
            return True

        problem_id = request.data["problem_id"]
        requested_problem = Problem.objects.filter(id=problem_id).first()

        if requested_problem is None:
            return True

        requested_contest = requested_problem.contest

        return (request.user.is_staff or request.user in requested_contest.participants.all()
                or request.user in requested_contest.contest_creator.all())
