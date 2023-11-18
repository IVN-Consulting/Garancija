from rest_framework import permissions


class CanViewWarrantyShopPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_view_shop_warranty' in request.user.get_all_permissions()


class CanViewWarrantyMyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_view_my_warranty' in request.user.get_all_permissions()


class ForbidPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
