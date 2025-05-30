from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'You are not owner of this entity'
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsLandlord(BasePermission):
    message = 'You are not Landlord, ask administrator for permission'
    def has_permission(self, request, view):
        return request.user.is_landlord