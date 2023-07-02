from rest_framework import permissions


class IsDoctor(permissions.BasePermission):

    def has_permission(self, request, view):
        # Check if the user has the 'doctor' role
        return request.user.is_authenticated and hasattr(request.user, 'doctor')


class IsPatient(permissions.BasePermission):

    def has_permission(self, request, view):
        # Check if the user has the 'Patient' role
        return request.user.is_authenticated and hasattr(request.user, 'patient')


class IsDoctor_Edit_Medical_Entry(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.doctor == request.user.doctor
