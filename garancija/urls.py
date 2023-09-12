from django.urls import path
from garancija import views

urlpatterns = [
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
    path('warranty', views.WarrantyView.as_view(), name="Warranty")
]
