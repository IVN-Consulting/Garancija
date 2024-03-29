"""
URL configuration for garancija project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from config import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("rest_framework_adresa", views.MyFirstEndpoint.as_view()),
    path("buda", views.Buda.as_view()),
    path("syncer", views.SyncerEndpoint.as_view()),
    path("api/", include("garancija.urls")),
    path("auth/", include("user.auth_urls")),
    path('silk/', include('silk.urls', namespace='silk'))
]
