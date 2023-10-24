from rest_framework import views, exceptions, viewsets, response, status
from garancija.models import Warranty, Employee, Shop
from garancija import serializers


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