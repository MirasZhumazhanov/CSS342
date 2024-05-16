from django.contrib import admin
from django.urls import path, include
from api.views import reg_page
urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),

]
