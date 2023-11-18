from django.urls import path
from garancija import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r'shops', views.ShopViewSet, basename="shops")
router.register(r'shops/(?P<shop_id>[0-9]*)/employees', views.EmployeesViewSet, basename="employees")
router.register(r'warranty', views.WarrantyViewSet, basename="warranty")
router.register(r'customers', views.CustomersViewSet, basename="customers")

urlpatterns = [
    *router.urls,
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
