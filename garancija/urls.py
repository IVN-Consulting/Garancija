from django.urls import path
from garancija import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'shops', views.ShopViewSet, basename="shops")
router.register(r'employees', views.EmployeesViewSet, basename="employees")
router.register(r'warranty', views.WarrantyViewSet, basename="warranty")


urlpatterns = [
    *router.urls,
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
    path('shop/<int:pk>/', views.ShopRetrieveDestroyView.as_view(), name='shop-retrieve-destroy'),
    path('shop/<int:id>/employees', views.EmployeesByShopView.as_view(), name="shop-employees"),
]
