from rest_framework.permissions import BasePermission

class IsCompanyUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == 'Company'

class IsJobSeekerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == 'Job Seeker'
