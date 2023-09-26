from rest_framework import views, response, generics, exceptions, viewsets, status
from garancija.models import Warranty, Employee, Shop
from garancija import serializers


class Healthcheck(views.APIView):
    def get(self, request):
        return response.Response("OK")

#WARRANTY VIEWS VVVVVVVVVVVVVVV
class WarrantyViewSet(viewsets.ModelViewSet):
    queryset = Warranty.objects.all()
    serializer_class = serializers.WarrantySerializer


#SHOP VIWS VVVVVVVVVVVVV

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer

#OVO SAM PRAVIO RUCNO JER NISAM ZNAO DA GA IMA U VIEWSET VVV
class ShopRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = serializers.ShopSerializer

    def delete(self, request, *args, **kwargs):
        shop = self.get_object()
        self.perform_destroy(shop)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

#EMPLOYEE VIWS VVVVVVVVVVVVV

class EmployeesViewSet(viewsets.ModelViewSet):
        queryset = Employee.objects.all()
        serializer_class = serializers.EmployeeSerializer

class EmployeesByShopView(generics.ListAPIView):
    serializer_class = serializers.EmployeeSerializer
    def get_queryset(self):
        try:
            shop_id = self.kwargs.get('id')
            shop = Shop.objects.get(id=shop_id)
            return Employee.objects.filter(shop=shop)
        except Shop.DoesNotExist:
            raise exceptions.NotFound










