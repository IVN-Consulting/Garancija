from rest_framework import views, exceptions, viewsets, response, status, permissions
from garancija.models import Warranty, Shop
from garancija import serializers, permissions as warranty_permissions
from user.models import User


class Healthcheck(views.APIView):
    def get(self, request):
        return response.Response("OK")


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer


class EmployeesViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action in ["create", 'update', 'partial_update', 'destroy']:
            return serializers.EmployeeWithoutShopSerializer
        else:
            return serializers.EmployeeSerializer

    def get_queryset(self):
        shop_id = int(self.kwargs['shop_id'])
        try:
            shop = Shop.objects.get(id=shop_id)
            return User.objects.filter(user_type="employee", shop=shop)
        except Shop.DoesNotExist:
            raise exceptions.NotFound


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(user_type="customer")
    serializer_class = serializers.CustomerSerializer


class WarrantyViewSet(viewsets.ModelViewSet):

    def get_queryset(self):

        objects = Warranty.objects\
            .select_related("salesperson__shop")\
            .select_related("customer__shop")\
            .prefetch_related("customer__groups__permissions")\
            .prefetch_related("salesperson__groups__permissions")\
            .prefetch_related("customer__user_permissions")\
            .prefetch_related("salesperson__user_permissions")

        if self.request.user.is_superuser:
            return objects.all()

        my_warranties = warranty_permissions.CanViewWarrantyMyPermission()
        if my_warranties.has_permission(self.request, self):
            return objects.filter(customer=self.request.user)

        shop_warranties = warranty_permissions.CanViewWarrantyShopPermission()
        if shop_warranties.has_permission(self.request, self):
            return objects.filter(salesperson__shop=self.request.user.shop)

        return objects.none()

    def get_permissions(self):
        can_view = warranty_permissions.CanViewWarrantyMyPermission | warranty_permissions.CanViewWarrantyShopPermission
        can_create = warranty_permissions.CanCreateWarrantyPermission
        can_edit = warranty_permissions.CanEditWarrantyPermission
        can_delete = warranty_permissions.CanDeleteWarrantyPermission
        if self.action in ['list', 'retrieve']:
            return permissions.IsAuthenticated(), can_view(),
        elif self.action == 'create':
            return permissions.IsAuthenticated(), can_create(),
        elif self.action in ['update', 'partial_update']:
            return permissions.IsAuthenticated(), can_edit(),
        elif self.action == 'destroy':
            return permissions.IsAuthenticated(), can_delete(),
        else:
            return permissions.IsAuthenticated(), warranty_permissions.ForbidPermission(),

    def get_serializer_class(self):
        if self.action in ["create", 'update', 'partial_update']:
            return serializers.CreateUpdateWarrantySerializer
        else:
            return serializers.ListWarrantySerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        warranty = Warranty.objects.get(id=serializer.data['id'])
        output_serializer = serializers.ListWarrantySerializer(warranty)
        output_data = output_serializer.data
        return response.Response(output_data, status=status.HTTP_201_CREATED)
