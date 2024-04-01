from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/', views.reg_page, name='registration'),
    path('login/', views.login_view, name='login'),
    path('', views.home_page, name='home'),
    path('log_out', views.logout_view, name='log_out'),
    path('profile/', views.profile, name='profile'),


    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('order', views.oprder_page, name='order')
]
