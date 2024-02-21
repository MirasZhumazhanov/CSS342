from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('crm.url')),
    path('admin/', admin.site.urls),
]
