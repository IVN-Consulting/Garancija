from django.contrib import admin
from garancija.models import Shop, Employee, Warranty




class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)

class WarrantyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Warranty, WarrantyAdmin)
