from rest_framework import permissions


class IsTheAgent(permissions.BasePermission):
    """
    Custom permission to only allow the agents of the clients to see it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.agent.user == request.user