from django.contrib import admin
from garancija.models import Shop, Warranty


class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'salesperson_username', 'customer_username')

    def salesperson_username(self, obj):
        return obj.salesperson.username

    def customer_username(self, obj):
        return obj.customer.username

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("salesperson__shop").select_related("customer")


admin.site.register(Warranty, WarrantyAdmin)
