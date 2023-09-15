from django.urls import path
from garancija import views

urlpatterns = [
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
    path('generics/warranty', views.WarrantyView.as_view(), name="generics-warranty"),
    path('shop', views.ShopListCreateView.as_view(), name="shop-list"),
    path('shop/<int:pk>/', views.ShopRetrieveView.as_view(), name='shop-retrieve')
    path('shop/<int:id>/employees', views.EmployeesByShopView.as_view(), name="shop-employees"),
]
