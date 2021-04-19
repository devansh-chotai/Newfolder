from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from . import views

# qty = all_products.get.qty
# print(all_products.template_name)
# all_products.qty
# {'extra_context':{'title':'something else'}}
# context = {'qty':qty}

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('mailing/', views.user_mailing_address, name='user_mailing_address'), 
    path('', views.user_account_info, name='user_account_info'),
    path('balance/', views.user_balance_info, name='user_balance_info'),
    path('changepassword/', views.PasswordChangeView.as_view(template_name='resetpassword.html'), name='change_password'),            
]