from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registration/', views.reg_page, name='registration'),
    path('login/', views.login_view, name='login'),
    path('', views.home_page, name='home'),
    path('log_out', views.logout_view, name='log_out'),
    path('profile/', views.profile, name='profile'),
    path('bookings/<int:pk>', views.get_bookings, name='bookings'),
    path('add_event/', views.add_event, name='add_event'),
    path('status/', views.status, name='status'),
    path('search/', views.search_billboards, name='search_page'),
    path('order/<int:pk>/', views.order_page, name='order_page'),
    path('payment/', views.payment, name='payment'),
    path('support/', views.support_page, name='support'),



    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('order/<int:pk>', views.order_page, name='order'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
