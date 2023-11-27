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


class ShopPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class CanViewShopEmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.user_type == "employee":
            shop_id = int(view.kwargs['shop_id'])
            if request.user.shop_id == shop_id:
                return 'user.can_view_shop_employee' in request.user.get_all_permissions()
            else:
                return False


class CanViewCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'user.can_view_customer' in request.user.get_all_permissions()


class IsSuperUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
