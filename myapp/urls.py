
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from SOCIAL_INTELLIGENT_AND_SAFETY import settings
from myapp import views

urlpatterns = [
    path('logout_page/',views.logout_page),
    path('public_page/',views.public_page),
    path('login_page/',views.login_page),

    path('admin_home/',views.admin_home),
    path('admin_home_sub/',views.admin_home_sub),
    path('change_password/',views.change_password),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('view_reels/', views.view_reels, name='view_reels'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('view_feedback/', views.view_feedback, name='view_feedback'),


# flutter======================









    path('update_location/', views.update_location, name='update_location'),
    path('update_location/', views.update_location, name='update_location'),
    path('app_login/', views.app_login, name='app_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('user_change_password/', views.user_change_password, name='user_change_password'),
    path('user_send_feedback/', views.user_send_feedback, name='user_send_feedback'),
    path('user_send_complaint/', views.user_send_complaint, name='user_send_complaint'),
    path('user_view_complaints/', views.user_view_complaints, name='user_view_complaints'),

]
