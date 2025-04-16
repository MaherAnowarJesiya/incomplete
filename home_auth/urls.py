














from django.contrib import admin
from django.urls import path
from . import views  # Fix this to import views properly

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),  # Use views.logout_view for consistency
]
