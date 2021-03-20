from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from django.views.static import serve
from users import views as users_views
urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('products.urls'), name= 'home' ),
    path('account/', include('accounts.urls')),
    path('signup/', users_views.signup, name='user_register'),
    path('mycart/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('static/<path>', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}), 
    path('media/<path>', serve , {'document_root': settings.MEDIA_ROOT, 'show_indexes': settings.DEBUG}), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)