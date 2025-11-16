# File: api/permissions.py
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Assumes the model instance has a 'user' attribute.
        return obj.user == request.user

class IsFinderOrClaimant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj here is a Claim instance
        return obj.found_item.finder == request.user or obj.claimant == request.user