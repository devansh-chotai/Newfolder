from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('mailing/', views.user_mailing_address, name='user_mailing_address'), 
    path('', views.user_account_info, name='user_account_info'),
    path('balance/', views.user_balance_info, name='user_balance_info'),            
]