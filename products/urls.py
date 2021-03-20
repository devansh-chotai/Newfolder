from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('search/', views.search_products, name='search_products'),
    path('product/(<slug>[\w-]+)/', views.single_product, name='single_product'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)