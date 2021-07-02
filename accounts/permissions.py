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


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # try:
        #     user = models.User.objects.get(pk=view.kwargs['pk'])
        #
        # except models.User.DoesNotExist:
        #     return False
        if request.user.pk != view.kwargs['pk']:
            return False
        return True


class IsOwnerToDeleteAddress(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            address = models.Address.objects.get(pk=view.kwargs['pk'])
        except models.Address.DoesNotExist:
            return False
        if request.user.pk != address.user.pk:
            return False

        return True


class IsOwnerToDeletePhone(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            address = models.Phone.objects.get(pk=view.kwargs['pk'])
        except models.Phone.DoesNotExist:
            return False
        if request.user.pk != address.user.pk:
            return False

        return True
