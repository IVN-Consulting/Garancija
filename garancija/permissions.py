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


class CanCreateWarrantyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_create_warranty' in request.user.get_all_permissions()


class CanEditWarrantyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_edit_warranty' in request.user.get_all_permissions()


class CanDeleteWarrantyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_delete_warranty' in request.user.get_all_permissions()
