from rest_framework import views, response, exceptions, viewsets, status
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
        if self.request.method == 'POST':  # bira serializer u odnosu na req
            return serializers.CreateWarrantySerializer
        else:
            return serializers.ListWarrantySerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)  # inicjalizuje serializer
        serializer.is_valid(raise_exception=True)  # proverava da data odg serializeru, ako ne dize gresku
        self.perform_create(serializer)  # pravi objekat sa data iz serializera
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # vraca novi objekad i status
