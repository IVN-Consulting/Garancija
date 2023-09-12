from rest_framework import views, response, generics
from garancija.models import Warranty, Employee, Shop
from garancija.serializers import WarrantySerializer

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
    serializer_class = WarrantySerializer
