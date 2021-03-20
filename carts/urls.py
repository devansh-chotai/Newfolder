from django.urls import path
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.my_cart, name='my_cart'),
    path('remove/(<cart_item_id>[\d]+)/', views.remove_item, name='remove_item'),
    path('media/<path>', serve , {'show_indexes': settings.DEBUG}), 

]