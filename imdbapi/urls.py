from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from imdbapp.api.v1 import urls as imdbapp_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'imdbapp/', include(imdbapp_urls))
]
