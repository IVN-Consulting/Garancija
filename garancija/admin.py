from django.contrib import admin
from garancija.models import Shop, Warranty


class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)


class WarrantyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Warranty, WarrantyAdmin)
