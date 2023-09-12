from rest_framework import views, response
from .models import Warranty, Employee, Shop

class Healthcheck(views.APIView):
    def get(self, request):
        return response.Response("OK")

class WarrantyView(views.APIView):
    def get(self, request):
        data = []
        for warranty in Warranty.objects.all():
            data.append({
                'id': warranty.id,
                'product_name': warranty.product_name,
                'shop': [
                    {
                        'shop_name': warranty.shop.name,
                        'shop_address': warranty.shop.address,
                        'salesperson': warranty.salesperson.name,

                    }
                ],
                'start_date': warranty.start_date,
                'end_date': warranty.end_date,
                'active': warranty.active
            })
        return response.Response(data)