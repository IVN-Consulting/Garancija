from django.contrib import admin
from garancija.models import Shop


class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)
