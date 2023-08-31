from django.contrib import admin
from garancija.models import Shop, Employee



class ShopAdmin(admin.ModelAdmin):
    pass


admin.site.register(Shop, ShopAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Employee, EmployeeAdmin)
