from rest_framework import views, response, generics, exceptions
from garancija.models import Warranty, Employee, Shop
from garancija import serializers


class Healthcheck(views.APIView):
    def get(self, request):
        return response.Response("OK")


class WarrantyViewBuda(views.APIView):
    def get(self, request):
        data = []
        for warranty in Warranty.objects.all():
            data.append({
                'id': warranty.id,
                'product_name': warranty.product_name,
                'shop': {
                    'shop_name': warranty.salesperson.shop.name,
                    'shop_address': warranty.salesperson.shop.address,
                    'salesperson': warranty.salesperson.name,
                },
                'start_date': warranty.start_date,
                'end_date': warranty.end_date
            })
        return response.Response(data)


class WarrantyView(generics.ListCreateAPIView):
    queryset = Warranty.objects.all()
    serializer_class = serializers.WarrantySerializer


class ShopListCreateView(generics.ListCreateAPIView):
    queryset = Shop.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ListShopSerializer
        elif self.request.method == 'POST':
            return serializers.CreateShopSerializer
        else:
            return super().get_serializer_class()

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        shop = Shop.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            address=validated_data['address'],
        )
        list_serializer = serializers.ListShopSerializer(instance=shop)
        return response.Response(list_serializer.data)

class ShopRetrieveView(generics.RetrieveAPIView):
    queryset = Shop.objects.all() #dao sam mu sve objekte shopa
    serializer_class = serializers.RetriveShopSerializer #povezivanje sa serializerom

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Shop.objects.get(pk=pk)
