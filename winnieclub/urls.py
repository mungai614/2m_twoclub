from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('winnieclubapp.urls')),  # Route all app URLs through club app
]
