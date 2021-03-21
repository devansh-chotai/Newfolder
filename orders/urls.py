from django.urls import path

from . import views

urlpatterns = [
    path('history/', views.my_orders, name='my_orders'),
    path('', views.new_orders, name='new_orders'),

]