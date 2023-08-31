from django.urls import path
from garancija import views

urlpatterns = [
    path('health', views.Healthcheck.as_view(), name="healthcheck"),
]
