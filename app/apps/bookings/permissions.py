from rest_framework.permissions import BasePermission

class IsLandlordOrAdmin(BasePermission):
    message = 'You are not a landlord of this property'
    def has_object_permission(self, request, view, obj):
        return obj.advertisement.owner == request.user or request.user.is_staff