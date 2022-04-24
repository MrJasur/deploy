from django.contrib import admin
from django.urls import path, include
from .views import home_page, landing_page
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home', home_page, name='home_page'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
    path('api/', include('api.urls')),

    #rest framework ishalshi uchun
    path('api-auth/', include('rest_framework.urls')),

    path('admin/', admin.site.urls),
]

#rasm bilan ishlash uchun
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)