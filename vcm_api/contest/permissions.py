from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsContestCreatorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (obj.contest_creator.filter(username=request.user.username).exists()
                or request.user.is_staff)
