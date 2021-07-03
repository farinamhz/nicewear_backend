from . import models
from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = models.User.objects.get(pk=request.data['user'])
        except models.User.DoesNotExist:
            return False

        if user.role == 2:
            return False
        return True


class IsUser2(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = models.User.objects.get(pk=view.kwargs['pk'])
        except models.User.DoesNotExist:
            return False

        if user.role == 2 or request.user.pk != user.pk:
            return False
        return True
