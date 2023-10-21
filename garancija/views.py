from rest_framework import views, exceptions, viewsets
from garancija.models import Warranty, Employee, Shop
from garancija import serializers
from rest_framework.response import Response


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
            return Employee.objects.filter(shop=shop)
        except Shop.DoesNotExist:
            raise exceptions.NotFound


class WarrantyViewSet(viewsets.ModelViewSet):
    queryset = Warranty.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", 'update']:
            return serializers.CreateUpdateWarrantySerializer
        elif self.action in ['partial_update']:
            return serializers.PartialUpdateWarrantySerializer
        else:
            return serializers.ListWarrantySerializer
