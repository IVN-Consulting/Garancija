from django.urls import path
from garancija import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'shops', views.ShopViewSet, basename="shops")
router.register(r'shops/(?P<shop_id>[0-9]*)/employees', views.EmployeesViewSet, basename="employees")
router.register(r'warranty', views.WarrantyViewSet, basename="warranty")
router.register(r'customers', views.CustomersViewSet, basename="customers")



urlpatterns = [
    *router.urls,
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
]
