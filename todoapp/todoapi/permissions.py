from rest_framework.permissions import BasePermission
from .models import TodoItem

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, TodoItem):
            return obj.owner == request.user
        return False
