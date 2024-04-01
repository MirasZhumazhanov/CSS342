from django.contrib import admin
from django.urls import path, include
from api.views import reg_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]
