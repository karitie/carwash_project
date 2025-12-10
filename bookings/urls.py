from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # User-facing URLs
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('booking/', views.booking, name='booking'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    # Admin panel URL
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('mark-complete/<int:booking_id>/', views.mark_complete, name='mark_complete'),
]